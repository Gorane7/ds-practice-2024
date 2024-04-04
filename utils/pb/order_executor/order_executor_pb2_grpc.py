# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import order_executor_pb2 as order__executor__pb2


class OrderExecutorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Token = channel.unary_unary(
                '/hello.OrderExecutor/Token',
                request_serializer=order__executor__pb2.TokenRequest.SerializeToString,
                response_deserializer=order__executor__pb2.TokenResponse.FromString,
                )
        self.Restart = channel.unary_unary(
                '/hello.OrderExecutor/Restart',
                request_serializer=order__executor__pb2.RestartRequest.SerializeToString,
                response_deserializer=order__executor__pb2.RestartResponse.FromString,
                )


class OrderExecutorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Token(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Restart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderExecutorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Token': grpc.unary_unary_rpc_method_handler(
                    servicer.Token,
                    request_deserializer=order__executor__pb2.TokenRequest.FromString,
                    response_serializer=order__executor__pb2.TokenResponse.SerializeToString,
            ),
            'Restart': grpc.unary_unary_rpc_method_handler(
                    servicer.Restart,
                    request_deserializer=order__executor__pb2.RestartRequest.FromString,
                    response_serializer=order__executor__pb2.RestartResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hello.OrderExecutor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrderExecutor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Token(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.OrderExecutor/Token',
            order__executor__pb2.TokenRequest.SerializeToString,
            order__executor__pb2.TokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Restart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.OrderExecutor/Restart',
            order__executor__pb2.RestartRequest.SerializeToString,
            order__executor__pb2.RestartResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
