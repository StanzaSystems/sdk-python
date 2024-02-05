# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from stanza.hub.v1 import usage_pb2 as stanza_dot_hub_dot_v1_dot_usage__pb2


class UsageServiceStub(object):
    """Used to get statistics on usage from Stanza, sliced and diced in various ways.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUsage = channel.unary_unary(
                '/stanza.hub.v1.UsageService/GetUsage',
                request_serializer=stanza_dot_hub_dot_v1_dot_usage__pb2.GetUsageRequest.SerializeToString,
                response_deserializer=stanza_dot_hub_dot_v1_dot_usage__pb2.GetUsageResponse.FromString,
                )


class UsageServiceServicer(object):
    """Used to get statistics on usage from Stanza, sliced and diced in various ways.
    """

    def GetUsage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UsageServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUsage': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUsage,
                    request_deserializer=stanza_dot_hub_dot_v1_dot_usage__pb2.GetUsageRequest.FromString,
                    response_serializer=stanza_dot_hub_dot_v1_dot_usage__pb2.GetUsageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'stanza.hub.v1.UsageService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UsageService(object):
    """Used to get statistics on usage from Stanza, sliced and diced in various ways.
    """

    @staticmethod
    def GetUsage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/stanza.hub.v1.UsageService/GetUsage',
            stanza_dot_hub_dot_v1_dot_usage__pb2.GetUsageRequest.SerializeToString,
            stanza_dot_hub_dot_v1_dot_usage__pb2.GetUsageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
