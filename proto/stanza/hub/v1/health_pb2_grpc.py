# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from stanza.hub.v1 import health_pb2 as stanza_dot_hub_dot_v1_dot_health__pb2


class HealthServiceStub(object):
    """The Health service definition. This service is used by the Stanza SDK to allow devs to
    make decisions about graceful degradation strategies to apply and to make decisions
    about fail-fast as high up the stack as possible.
    "Keys" - API bearer tokens - are not included in API and should be sent via a X-Stanza-Key header.
    Customer IDs are determined based on the X-Stanza-Key header (each key is associated
    with one and only one customer).
    However, env must always be specified - stanza keys do not have to be
    specific to an environment, so we cannot infer the env from the key.
    Like quota service this should be accessed by SDK via HTTPS.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.QueryDecoratorHealth = channel.unary_unary(
                '/stanza.hub.v1.HealthService/QueryDecoratorHealth',
                request_serializer=stanza_dot_hub_dot_v1_dot_health__pb2.QueryDecoratorHealthRequest.SerializeToString,
                response_deserializer=stanza_dot_hub_dot_v1_dot_health__pb2.QueryDecoratorHealthResponse.FromString,
                )


class HealthServiceServicer(object):
    """The Health service definition. This service is used by the Stanza SDK to allow devs to
    make decisions about graceful degradation strategies to apply and to make decisions
    about fail-fast as high up the stack as possible.
    "Keys" - API bearer tokens - are not included in API and should be sent via a X-Stanza-Key header.
    Customer IDs are determined based on the X-Stanza-Key header (each key is associated
    with one and only one customer).
    However, env must always be specified - stanza keys do not have to be
    specific to an environment, so we cannot infer the env from the key.
    Like quota service this should be accessed by SDK via HTTPS.
    """

    def QueryDecoratorHealth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HealthServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'QueryDecoratorHealth': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryDecoratorHealth,
                    request_deserializer=stanza_dot_hub_dot_v1_dot_health__pb2.QueryDecoratorHealthRequest.FromString,
                    response_serializer=stanza_dot_hub_dot_v1_dot_health__pb2.QueryDecoratorHealthResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'stanza.hub.v1.HealthService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class HealthService(object):
    """The Health service definition. This service is used by the Stanza SDK to allow devs to
    make decisions about graceful degradation strategies to apply and to make decisions
    about fail-fast as high up the stack as possible.
    "Keys" - API bearer tokens - are not included in API and should be sent via a X-Stanza-Key header.
    Customer IDs are determined based on the X-Stanza-Key header (each key is associated
    with one and only one customer).
    However, env must always be specified - stanza keys do not have to be
    specific to an environment, so we cannot infer the env from the key.
    Like quota service this should be accessed by SDK via HTTPS.
    """

    @staticmethod
    def QueryDecoratorHealth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/stanza.hub.v1.HealthService/QueryDecoratorHealth',
            stanza_dot_hub_dot_v1_dot_health__pb2.QueryDecoratorHealthRequest.SerializeToString,
            stanza_dot_hub_dot_v1_dot_health__pb2.QueryDecoratorHealthResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
