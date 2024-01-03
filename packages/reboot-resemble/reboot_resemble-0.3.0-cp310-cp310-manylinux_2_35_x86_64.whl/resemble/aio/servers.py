from __future__ import annotations

import grpc
import logging
import os
from google.protobuf.descriptor import FileDescriptor
from google.protobuf.descriptor_pb2 import FileDescriptorSet
from grpc_reflection.v1alpha import reflection
from resemble.aio.internals.channel_manager import _ChannelManager
from resemble.aio.internals.middleware import Middleware
from resemble.aio.internals.tasks_cache import TasksCache
from resemble.aio.internals.tasks_servicer import TasksServicer
from resemble.aio.react import ReactServicer
from resemble.aio.resolvers import ActorResolver, StaticResolver
from resemble.aio.servicers import (
    ConfigServicer,
    ResembleServiceable,
    Routable,
    Serviceable,
    Servicer,
)
from resemble.aio.state_managers import LocalSidecarStateManager, StateManager
from resemble.aio.types import RoutableAddress, ServiceName
from resemble.aio.workflows import Workflow
from resemble.controller.settings import (
    ENVVAR_RESEMBLE_CONFIG_SERVER_PORT,
    ENVVAR_RESEMBLE_MODE,
    ENVVAR_RESEMBLE_SYSTEM_NAMESPACE,
    RESEMBLE_MODE_CONFIG,
    RESEMBLE_ROUTABLE_HOSTNAME,
    USER_CONTAINER_PORT,
)
from resemble.helpers import (
    base64_serialize_proto_descriptor_set,
    generate_proto_descriptor_set,
)
from resemble.inspect.servicer import InspectServicer
from resemble.settings import RESEMBLE_STATE_DIRECTORY
from resemble.v1alpha1 import react_pb2, server_config_pb2
from resemble.v1alpha1.inspect.inspect_rsm import Inspect
from typing import Optional


class Server:
    """Server is expected to be used in a container's `main()` method; its
    purpose is to start serving the Resemble servicers that make up an
    application. For example:
    ```
        async def main():
            server = Server.create(servicers=[Foo, Bar])
            await server.run()


        if __name__ == '__main__':
            asyncio.run(main())
    ```
    """

    def __init__(self, listen_address: RoutableAddress):
        if type(self) == Server:
            # The user called the constructor directly; otherwise we'd be a
            # _ServiceServer or _ConfigServer or similar.
            raise ValueError(
                'Do not construct Server directly; use Server.create()'
            )
        grpc_server = grpc.aio.server()

        try:
            host, port = listen_address.split(':')
        except ValueError:
            host = listen_address

        port = grpc_server.add_insecure_port(listen_address)
        # TODO: Resolve the address (if possible) to a routable address.
        # The address 0.0.0.0 means listen on all network interfaces (there
        # could be more/many/ambiguity). It would be nice to resolve it into
        # something we can use in a test (like 127.0.0.1).
        address = f'{host}:{port}'
        self._grpc_server: grpc.aio.server = grpc_server
        self._listen_address: RoutableAddress = address

    @classmethod
    def create(
        cls,
        servicers: list[type[Servicer]],
        listen_address: RoutableAddress = '127.0.0.1:0',
    ) -> Server:
        serviceables = [
            Serviceable.from_servicer_type(servicer_type)
            for servicer_type in servicers
        ]
        # To prevent typos mixing up `servicers` and `serviceables`, delete
        # `servicers` (so that mypy can catch if we accidentally use it).
        del servicers

        # Depending on which mode we're starting in, serving or config, we
        # either instantiate a _ServiceServer for handling user requests or a
        # _ConfigServer which is used internally to configure out system.
        if os.environ.get(ENVVAR_RESEMBLE_MODE) == RESEMBLE_MODE_CONFIG:
            server_port = os.environ.get(ENVVAR_RESEMBLE_CONFIG_SERVER_PORT)
            if server_port is None:
                raise EnvironmentError(
                    f'{ENVVAR_RESEMBLE_CONFIG_SERVER_PORT} not found. Must be present '
                    f'when {ENVVAR_RESEMBLE_MODE} is `{RESEMBLE_MODE_CONFIG}`.'
                )

            listen_address = f'0.0.0.0:{server_port}'
            return _ConfigServer(
                serviceables=serviceables,
                listen_address=listen_address,
            )
        # We're not in config mode, so we'll be serving as a consensus member.

        system_namespace = os.environ.get(ENVVAR_RESEMBLE_SYSTEM_NAMESPACE)
        if system_namespace is None:
            raise EnvironmentError(
                f'{ENVVAR_RESEMBLE_SYSTEM_NAMESPACE} not found. Must be present '
                f'when {ENVVAR_RESEMBLE_MODE} is not `{RESEMBLE_MODE_CONFIG}`.'
            )
        # Route all traffic to the Resemble routable hostname. We rely on Istio
        # and our EnvoyFilters to route the traffic to the appropriate
        # consensus.
        static_routable_address = f'{RESEMBLE_ROUTABLE_HOSTNAME}.{system_namespace}:{USER_CONTAINER_PORT}'
        logging.debug(
            f'Routing all actor traffic to address: {static_routable_address}'
        )
        actor_resolver = StaticResolver(static_routable_address)

        # TODO(rjh): use SidecarStateManager once launching sidecars as separate
        #            k8s pods instead of in-process?
        state_manager = LocalSidecarStateManager(RESEMBLE_STATE_DIRECTORY)

        # TODO: Consider pulling this file_descriptor_set info out of a
        # corresponding ServerConfig rather than regenerating it from
        # serviceables here.
        file_descriptor_set = generate_proto_descriptor_set(
            routables=serviceables
        )

        return _ServiceServer(
            serviceables=serviceables,
            listen_address=listen_address,
            state_manager=state_manager,
            actor_resolver=actor_resolver,
            file_descriptor_set=file_descriptor_set
        )

    async def wait(self):
        await self._grpc_server.wait_for_termination()

    def port(self) -> int:
        """Return port of gRPC server."""
        # Note: Formatting of the address string is done through the factory
        # method. There should be no case in which this is undefined or results
        # in an index or type error.
        return int(self._listen_address.split(':')[-1])

    async def start(self):
        """Start server."""
        # Note: In the future we might have pre/post start hooks here for
        # servicers.
        await self._grpc_server.start()

    async def stop(self, gracetime: Optional[float] = None):
        """Stop grpc server."""
        # Note: In the future we might have pre/post stop hooks here for
        # servicers.
        await self._grpc_server.stop(grace=gracetime)

    async def run(self):
        await self.start()
        await self.wait()


class _ServiceServer(Server):

    class ReactRoutable(Routable):
        """Helper "routable" that can be provided to for routing to the
        `ReactServicer` system service that we run manually."""

        def service_name(self) -> ServiceName:
            # TODO(benh): get from react_pb2.DESCRIPTOR.
            return 'resemble.v1alpha1.React'

        def file_descriptor(self) -> FileDescriptor:
            return react_pb2.DESCRIPTOR.services_by_name['React'].file

    ROUTABLES: list[Routable] = [
        ReactRoutable(),

        # We also manually run the `InspectServicer`, and thus we need
        # to expose it as a "routable" so it can be routed to.
        Serviceable.from_servicer_type(InspectServicer),
    ]

    _websocket_port: Optional[int]

    def __init__(
        self,
        serviceables: list[Serviceable],
        listen_address: RoutableAddress,
        state_manager: StateManager,
        actor_resolver: ActorResolver,
        file_descriptor_set: FileDescriptorSet,
    ):
        super().__init__(listen_address)

        self._state_manager = state_manager
        self._channel_manager = _ChannelManager(
            actor_resolver,
            # Communication between actors does not use a secure channel,
            # since it doesn't go through the gateway, which is where SSL
            # termination happens. In production infrastructure it is assumed
            # that this intra-Resemble traffic is secured otherwise, e.g. via Istio
            # sidecars providing mTLS.
            secure=False,
        )
        self._file_descriptor_set = file_descriptor_set

        # Keep track of our middleware so that we can use it to manually
        # dispatch recovered tasks.
        self._middleware_by_service_name: dict[ServiceName, Middleware] = {}

        # Construct shared tasks cache.
        tasks_cache = TasksCache()

        # Now start serving the serviceables.
        for serviceable in serviceables:
            if isinstance(serviceable, ResembleServiceable):
                # Resemble servicers get middleware. Requests are passed to the
                # middleware, which will pass them on to the user code.
                servicer, _ = serviceable.instantiate()
                middleware = servicer.create_middleware(
                    self._state_manager, self._channel_manager, tasks_cache
                )
                middleware.add_to_server(self._grpc_server)
                self._middleware_by_service_name[servicer.__service_name__
                                                ] = middleware
            else:
                # Legacy gRPC servicers don't get middleware. Requests are
                # passed to the user code directly.
                legacy_grpc_servicer, add_to_server = serviceable.instantiate()
                assert add_to_server is not None
                add_to_server(legacy_grpc_servicer, self._grpc_server)

        # Construct 'Inspect' system service (also a Resemble service
        # so needs to be added _before_ creating the 'React' system
        # service).
        self._inspect_servicer = InspectServicer(
            self._state_manager,
            self._middleware_by_service_name,
        )

        middleware = self._inspect_servicer.create_middleware(
            self._state_manager, self._channel_manager, tasks_cache
        )
        middleware.add_to_server(self._grpc_server)
        self._middleware_by_service_name[
            self._inspect_servicer.__service_name__] = middleware

        # Construct and add 'React' system service for the Resemble servicers.
        #
        # Invariant: `self._middleware_by_service_name` has been fully
        # constructed at this point.
        self._react_servicer = ReactServicer(self._middleware_by_service_name)
        self._react_servicer.add_to_server(self._grpc_server)

        self._websocket_port = None

        # Construct and add 'Tasks' system service.
        self._tasks_servicer = TasksServicer(self._state_manager, tasks_cache)
        self._tasks_servicer.add_to_server(self._grpc_server)

        # Add StateManager system services (i.e., to serve transaction
        # coordinators and participants).
        state_manager.add_to_server(self._grpc_server)

        # We use the reflection service to make this server more debugable. See:
        # https://github.com/grpc/grpc/blob/master/doc/python/server_reflection.md
        service_names = tuple([s.service_name() for s in serviceables])
        reflection.enable_server_reflection(service_names, self._grpc_server)

    async def start(self):
        # Recover past state (if any).
        await self._state_manager.recover(
            self._channel_manager,
            self._middleware_by_service_name,
            self._file_descriptor_set,
        )

        # Once recovery is complete, we can start serving traffic.
        await super().start()

        # And also start serving React traffic.
        self._websocket_port = await self._react_servicer.start()

        # Call 'Inspect.Create' which is specifically just a writer
        # (not a constructor) so that we can call it every time to
        # ensure it is constructed.
        workflow = Workflow(
            name="Ensure 'Inspect' is created",
            gateway=self._listen_address,
            # Not using a secure channel, since our `gateway` is in fact the
            # (non-SSL) port of the actual service.
            secure_channel=False,
        )

        # TODO(benh): replace with singleton so that we don't
        # need to instantiate it here.
        await Inspect(InspectServicer.SINGLETON_ACTOR_ID).Create(workflow)

    async def stop(self, gracetime: Optional[float] = None):
        # Stop any background tasks running in the middleware.
        for middleware in self._middleware_by_service_name.values():
            await middleware.stop()

        # Stop serving React traffic.
        await self._react_servicer.stop()

        # Stop serving traffic.
        await super().stop(gracetime=gracetime)

    def websocket_port(self) -> int:
        """Return port of React websocket server."""
        if self._websocket_port is None:
            raise RuntimeError(
                'Must call `start()` before trying to get websocket port'
            )

        return self._websocket_port


class _ConfigServer(Server):

    def __init__(
        self,
        serviceables: list[Serviceable],
        listen_address: RoutableAddress,
    ):
        super().__init__(listen_address)

        proto_descriptor_set = generate_proto_descriptor_set(
            routables=serviceables
        )
        service_names = [s.service_name() for s in serviceables]
        server_config = server_config_pb2.ServerConfig(
            file_descriptor_set=base64_serialize_proto_descriptor_set(
                proto_descriptor_set
            ),
            service_names=service_names
        )

        ConfigServicer.add_to_server(self._grpc_server, server_config)
