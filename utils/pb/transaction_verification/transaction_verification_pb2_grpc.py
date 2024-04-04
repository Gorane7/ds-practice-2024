# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import transaction_verification_pb2 as transaction__verification__pb2


class VerifServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Verify = channel.unary_unary(
                '/hello.VerifService/Verify',
                request_serializer=transaction__verification__pb2.VerifyRequest.SerializeToString,
                response_deserializer=transaction__verification__pb2.VerifyResponse.FromString,
                )
        self.VectorClockUpdate = channel.unary_unary(
                '/hello.VerifService/VectorClockUpdate',
                request_serializer=transaction__verification__pb2.VectorClockInp_trans.SerializeToString,
                response_deserializer=transaction__verification__pb2.Empty_trans.FromString,
                )
        self.Kill = channel.unary_unary(
                '/hello.VerifService/Kill',
                request_serializer=transaction__verification__pb2.KillOrder_trans.SerializeToString,
                response_deserializer=transaction__verification__pb2.Empty_trans.FromString,
                )


class VerifServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Verify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorClockUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Kill(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VerifServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Verify': grpc.unary_unary_rpc_method_handler(
                    servicer.Verify,
                    request_deserializer=transaction__verification__pb2.VerifyRequest.FromString,
                    response_serializer=transaction__verification__pb2.VerifyResponse.SerializeToString,
            ),
            'VectorClockUpdate': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorClockUpdate,
                    request_deserializer=transaction__verification__pb2.VectorClockInp_trans.FromString,
                    response_serializer=transaction__verification__pb2.Empty_trans.SerializeToString,
            ),
            'Kill': grpc.unary_unary_rpc_method_handler(
                    servicer.Kill,
                    request_deserializer=transaction__verification__pb2.KillOrder_trans.FromString,
                    response_serializer=transaction__verification__pb2.Empty_trans.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hello.VerifService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VerifService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Verify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.VerifService/Verify',
            transaction__verification__pb2.VerifyRequest.SerializeToString,
            transaction__verification__pb2.VerifyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorClockUpdate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.VerifService/VectorClockUpdate',
            transaction__verification__pb2.VectorClockInp_trans.SerializeToString,
            transaction__verification__pb2.Empty_trans.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Kill(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.VerifService/Kill',
            transaction__verification__pb2.KillOrder_trans.SerializeToString,
            transaction__verification__pb2.Empty_trans.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
