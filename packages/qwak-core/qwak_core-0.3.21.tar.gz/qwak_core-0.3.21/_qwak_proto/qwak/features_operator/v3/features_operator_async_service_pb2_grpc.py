# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from _qwak_proto.qwak.features_operator.v3 import features_operator_async_service_pb2 as qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2


class FeaturesOperatorAsyncServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ValidateDataSource = channel.unary_unary(
                '/qwak.features_operator.v3.FeaturesOperatorAsyncService/ValidateDataSource',
                request_serializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidateDataSourceRequest.SerializeToString,
                response_deserializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidationResponse.FromString,
                )
        self.ValidateFeatureSet = channel.unary_unary(
                '/qwak.features_operator.v3.FeaturesOperatorAsyncService/ValidateFeatureSet',
                request_serializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidateFeatureSetRequest.SerializeToString,
                response_deserializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidationResponse.FromString,
                )
        self.GetValidationResult = channel.unary_unary(
                '/qwak.features_operator.v3.FeaturesOperatorAsyncService/GetValidationResult',
                request_serializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.GetValidationResultRequest.SerializeToString,
                response_deserializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.GetValidationResultResponse.FromString,
                )
        self.CancelValidation = channel.unary_unary(
                '/qwak.features_operator.v3.FeaturesOperatorAsyncService/CancelValidation',
                request_serializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.CancelValidationRequest.SerializeToString,
                response_deserializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.CancelValidationResponse.FromString,
                )


class FeaturesOperatorAsyncServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ValidateDataSource(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidateFeatureSet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetValidationResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelValidation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FeaturesOperatorAsyncServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ValidateDataSource': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateDataSource,
                    request_deserializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidateDataSourceRequest.FromString,
                    response_serializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidationResponse.SerializeToString,
            ),
            'ValidateFeatureSet': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateFeatureSet,
                    request_deserializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidateFeatureSetRequest.FromString,
                    response_serializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidationResponse.SerializeToString,
            ),
            'GetValidationResult': grpc.unary_unary_rpc_method_handler(
                    servicer.GetValidationResult,
                    request_deserializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.GetValidationResultRequest.FromString,
                    response_serializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.GetValidationResultResponse.SerializeToString,
            ),
            'CancelValidation': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelValidation,
                    request_deserializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.CancelValidationRequest.FromString,
                    response_serializer=qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.CancelValidationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'qwak.features_operator.v3.FeaturesOperatorAsyncService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FeaturesOperatorAsyncService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ValidateDataSource(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.features_operator.v3.FeaturesOperatorAsyncService/ValidateDataSource',
            qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidateDataSourceRequest.SerializeToString,
            qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ValidateFeatureSet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.features_operator.v3.FeaturesOperatorAsyncService/ValidateFeatureSet',
            qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidateFeatureSetRequest.SerializeToString,
            qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.ValidationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetValidationResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.features_operator.v3.FeaturesOperatorAsyncService/GetValidationResult',
            qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.GetValidationResultRequest.SerializeToString,
            qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.GetValidationResultResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelValidation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.features_operator.v3.FeaturesOperatorAsyncService/CancelValidation',
            qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.CancelValidationRequest.SerializeToString,
            qwak_dot_features__operator_dot_v3_dot_features__operator__async__service__pb2.CancelValidationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
