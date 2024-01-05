# The settings below must match their equivalents, if applicable, in:
# * resemble/settings.h
# * <possibly other languages by the time you read this>

# gRPC max message size to transmit large actor state data.
MAX_SIDECAR_GRPC_MESSAGE_LENGTH_BYTES = 100 * 1024 * 1024

ENVOY_PROXY_IMAGE = 'envoyproxy/envoy:v1.24.0'

# The path to the directory where Resemble state is stored.
RESEMBLE_STATE_DIRECTORY = '/var/run/resemble/state'
