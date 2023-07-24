# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from stanza.hub.v1 import quota_pb2 as stanza_dot_hub_dot_v1_dot_quota__pb2


class QuotaServiceStub(object):
    """This protocol buffer definition is the source of truth for the Stanza Hub Quota API.
    There is also an OpenAPI spec, generated via https://github.com/grpc-ecosystem/grpc-gateway.

    Quota service is a centralised ratelimiting service, used by Stanza and Browser SDKs to determine whether a given request should be permitted, or whether a Feature should be displayed.

    The Quota service definition. This service is used by the Stanza and Browser SDKs to determine whether quota is available to use services which are subject to centralised ratelimiting.
    "Keys" are not included in API and should be sent via a X-Stanza-Key header.
    Customer IDs are determined based on the X-Stanza-Key header (each key is associated with one and only one customer). However, environment must always be specified when requesting a token - Stanza keys do not have to be specific to an environment, so we cannot infer that from the key alone.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetToken = channel.unary_unary(
                '/stanza.hub.v1.QuotaService/GetToken',
                request_serializer=stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenRequest.SerializeToString,
                response_deserializer=stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenResponse.FromString,
                )
        self.GetTokenLease = channel.unary_unary(
                '/stanza.hub.v1.QuotaService/GetTokenLease',
                request_serializer=stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenLeaseRequest.SerializeToString,
                response_deserializer=stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenLeaseResponse.FromString,
                )
        self.SetTokenLeaseConsumed = channel.unary_unary(
                '/stanza.hub.v1.QuotaService/SetTokenLeaseConsumed',
                request_serializer=stanza_dot_hub_dot_v1_dot_quota__pb2.SetTokenLeaseConsumedRequest.SerializeToString,
                response_deserializer=stanza_dot_hub_dot_v1_dot_quota__pb2.SetTokenLeaseConsumedResponse.FromString,
                )
        self.ValidateToken = channel.unary_unary(
                '/stanza.hub.v1.QuotaService/ValidateToken',
                request_serializer=stanza_dot_hub_dot_v1_dot_quota__pb2.ValidateTokenRequest.SerializeToString,
                response_deserializer=stanza_dot_hub_dot_v1_dot_quota__pb2.ValidateTokenResponse.FromString,
                )


class QuotaServiceServicer(object):
    """This protocol buffer definition is the source of truth for the Stanza Hub Quota API.
    There is also an OpenAPI spec, generated via https://github.com/grpc-ecosystem/grpc-gateway.

    Quota service is a centralised ratelimiting service, used by Stanza and Browser SDKs to determine whether a given request should be permitted, or whether a Feature should be displayed.

    The Quota service definition. This service is used by the Stanza and Browser SDKs to determine whether quota is available to use services which are subject to centralised ratelimiting.
    "Keys" are not included in API and should be sent via a X-Stanza-Key header.
    Customer IDs are determined based on the X-Stanza-Key header (each key is associated with one and only one customer). However, environment must always be specified when requesting a token - Stanza keys do not have to be specific to an environment, so we cannot infer that from the key alone.
    """

    def GetToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTokenLease(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetTokenLeaseConsumed(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidateToken(self, request, context):
        """Used by ingress decorators to validate Hub-generated tokens.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QuotaServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetToken': grpc.unary_unary_rpc_method_handler(
                    servicer.GetToken,
                    request_deserializer=stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenRequest.FromString,
                    response_serializer=stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenResponse.SerializeToString,
            ),
            'GetTokenLease': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTokenLease,
                    request_deserializer=stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenLeaseRequest.FromString,
                    response_serializer=stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenLeaseResponse.SerializeToString,
            ),
            'SetTokenLeaseConsumed': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTokenLeaseConsumed,
                    request_deserializer=stanza_dot_hub_dot_v1_dot_quota__pb2.SetTokenLeaseConsumedRequest.FromString,
                    response_serializer=stanza_dot_hub_dot_v1_dot_quota__pb2.SetTokenLeaseConsumedResponse.SerializeToString,
            ),
            'ValidateToken': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateToken,
                    request_deserializer=stanza_dot_hub_dot_v1_dot_quota__pb2.ValidateTokenRequest.FromString,
                    response_serializer=stanza_dot_hub_dot_v1_dot_quota__pb2.ValidateTokenResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'stanza.hub.v1.QuotaService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class QuotaService(object):
    """This protocol buffer definition is the source of truth for the Stanza Hub Quota API.
    There is also an OpenAPI spec, generated via https://github.com/grpc-ecosystem/grpc-gateway.

    Quota service is a centralised ratelimiting service, used by Stanza and Browser SDKs to determine whether a given request should be permitted, or whether a Feature should be displayed.

    The Quota service definition. This service is used by the Stanza and Browser SDKs to determine whether quota is available to use services which are subject to centralised ratelimiting.
    "Keys" are not included in API and should be sent via a X-Stanza-Key header.
    Customer IDs are determined based on the X-Stanza-Key header (each key is associated with one and only one customer). However, environment must always be specified when requesting a token - Stanza keys do not have to be specific to an environment, so we cannot infer that from the key alone.
    """

    @staticmethod
    def GetToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/stanza.hub.v1.QuotaService/GetToken',
            stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenRequest.SerializeToString,
            stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTokenLease(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/stanza.hub.v1.QuotaService/GetTokenLease',
            stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenLeaseRequest.SerializeToString,
            stanza_dot_hub_dot_v1_dot_quota__pb2.GetTokenLeaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetTokenLeaseConsumed(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/stanza.hub.v1.QuotaService/SetTokenLeaseConsumed',
            stanza_dot_hub_dot_v1_dot_quota__pb2.SetTokenLeaseConsumedRequest.SerializeToString,
            stanza_dot_hub_dot_v1_dot_quota__pb2.SetTokenLeaseConsumedResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ValidateToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/stanza.hub.v1.QuotaService/ValidateToken',
            stanza_dot_hub_dot_v1_dot_quota__pb2.ValidateTokenRequest.SerializeToString,
            stanza_dot_hub_dot_v1_dot_quota__pb2.ValidateTokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
