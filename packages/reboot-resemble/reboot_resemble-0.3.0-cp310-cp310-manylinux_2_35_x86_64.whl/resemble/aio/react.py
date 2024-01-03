import asyncio
import grpc
import json
import logging
import traceback
import websockets
from google.protobuf import any_pb2
from google.protobuf.json_format import MessageToJson
from google.rpc import code_pb2, status_pb2
from grpc_status import rpc_status
from resemble.aio.errors import Aborted, Error, UnknownService
from resemble.aio.headers import Headers
from resemble.aio.internals.middleware import Middleware
from resemble.aio.types import ServiceName
from resemble.v1alpha1 import react_pb2, react_pb2_grpc
from respect.logging import get_logger
from typing import AsyncIterable, Optional

logger = get_logger(__name__)

# We set the log level to `ERROR` here because websockets is chatty!
logger.setLevel(logging.ERROR)


class ReactServicer(react_pb2_grpc.ReactServicer):
    """System service for serving requests from our code generated react
    readers.

    TODO(benh): make this more generic than just for react so that
    users and other system services (e.g., a read cache) can use this
    to get reactive/streaming reads without the user having to
    implement it themselves.
    """

    def __init__(
        self, middleware_by_service_name: dict[ServiceName, Middleware]
    ):
        self._middleware_by_service_name = middleware_by_service_name

        self._stop_websockets_serve = asyncio.Event()

    async def start(self) -> int:
        """Starts the websocket server and returns the port that it is
        listening on."""
        port: asyncio.Future[int] = asyncio.Future()

        async def websockets_serve():
            async with websockets.serve(
                self.serve, '127.0.0.1', logger=logger
            ) as server:
                port.set_result(server.sockets[0].getsockname()[1])
                await self._stop_websockets_serve.wait()

        self._websockets_serve_task = asyncio.create_task(websockets_serve())

        await port

        return port.result()

    async def stop(self):
        self._stop_websockets_serve.set()
        try:
            await self._websockets_serve_task
        except:
            # We're trying to stop so no need to propagate any
            # exceptions.
            pass

    async def serve(self, websocket):
        # Expected path: /__/resemble/websocket/service_name/actor_id
        #
        # After split: ['', '__', 'resemble' 'websocket', 'service_name', 'actor_id']
        service_name, actor_id = websocket.path.split('/')[4:6]

        middleware: Optional[Middleware] = (
            self._middleware_by_service_name.get(service_name)
        )

        if middleware is None:
            logger.error(
                "Attempted to perform a 'React' mutate to an unknown "
                f"service '{service_name}'; "
                "did you bring up a servicer for it in your `Application`?"
            )
            raise Error(UnknownService())

        try:
            async for request_bytes in websocket:
                try:
                    request = react_pb2.MutateRequest()
                    request.ParseFromString(request_bytes)

                    response = await middleware.react_mutate(
                        actor_id,
                        request.method,
                        request.request,
                        request.idempotency_key,
                    )

                    await websocket.send(
                        react_pb2.MutateResponse(
                            response=response.SerializeToString()
                        ).SerializeToString()
                    )
                except Aborted as aborted:
                    status = aborted.to_status(
                        # NOTE: we don't pass `error_type` which means
                        # we'll get a different error message than
                        # when an error is returned within Resemble.
                    )
                    await websocket.send(
                        react_pb2.MutateResponse(status=MessageToJson(status)
                                                ).SerializeToString()
                    )
                except BaseException as exception:
                    # TODO: send a status which does not include any
                    # details, just a message which we glean from the
                    # raised exception.
                    status = status_pb2.Status(
                        code=code_pb2.Code.UNKNOWN,
                        message=f'{type(exception).__name__}: {exception}',
                    )
                    await websocket.send(
                        react_pb2.MutateResponse(status=MessageToJson(status)
                                                ).SerializeToString()
                    )
        except websockets.exceptions.ConnectionClosedOK:
            # No real error here, browser users will come and go!
            pass
        except websockets.exceptions.ConnectionClosedError:
            # No real error here, browser users may get disconnected!
            pass
        except:
            # For now we print these out so we can debug if necessary.
            traceback.print_exc()

    def add_to_server(self, server: grpc.aio.Server) -> None:
        react_pb2_grpc.add_ReactServicer_to_server(self, server)

    async def Query(
        self,
        request: react_pb2.QueryRequest,
        grpc_context: grpc.aio.ServicerContext,
    ) -> AsyncIterable[react_pb2.QueryResponse]:
        """Implements the React.Query RPC that calls into the
        'Middleware.react' method for handling the request."""
        try:
            headers = Headers.from_grpc_context(grpc_context)

            middleware: Optional[Middleware] = (
                self._middleware_by_service_name.get(headers.service_name)
            )

            if middleware is None:
                logger.error(
                    "Attempted to perform a 'React' query to an unknown "
                    f"service '{headers.service_name}'; "
                    "did you bring up a servicer for it in your `Application`?"
                )
                raise Error(UnknownService())

            async for (response, idempotency_keys) in middleware.react_query(
                grpc_context,
                headers.actor_id,
                request.method,
                request.request,
            ):
                yield react_pb2.QueryResponse(
                    response=(
                        response.SerializeToString()
                        if response is not None else None
                    ),
                    idempotency_keys=[
                        str(idempotency_key)
                        for idempotency_key in idempotency_keys
                    ],
                )
        except asyncio.CancelledError:
            # It's pretty normal for a query to be cancelled; it's not useful to
            # print a stack trace.
            raise
        except Aborted as aborted:
            await grpc_context.abort_with_status(
                rpc_status.to_status(
                    aborted.to_status(
                        # NOTE: we don't pass `error_type` which means
                        # we'll get a different error message than
                        # when an error is returned within Resemble.
                    )
                )
            )
        except:
            # Don't print a stack trace for any common errors or user
            # errors that were raised that we turned into an
            # `Aborted`. We should have logged an error to make it
            # easier for a user to debug.
            #
            # As of the writing of this comment we know that if the
            # context status code is `ABORTED` then it must have been
            # from our `Aborted` because there aren't any other ways
            # for Resemble apps to abort an RPC because we don't give
            # them access to a `ServicerContext`. But even if we do,
            # if a user calls abort then that's similar to raising one
            # of their user errors and we probably don't need to print
            # a stack trace.
            if grpc_context.code() != code_pb2.Code.ABORTED:
                traceback.print_exc()

            raise
