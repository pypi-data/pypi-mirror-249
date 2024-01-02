# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from vdp.controller.v1beta import controller_pb2 as vdp_dot_controller_dot_v1beta_dot_controller__pb2


class ControllerPrivateServiceStub(object):
    """Controller service responds to incoming controller requests
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Liveness = channel.unary_unary(
                '/vdp.controller.v1beta.ControllerPrivateService/Liveness',
                request_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.LivenessRequest.SerializeToString,
                response_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.LivenessResponse.FromString,
                )
        self.Readiness = channel.unary_unary(
                '/vdp.controller.v1beta.ControllerPrivateService/Readiness',
                request_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.ReadinessRequest.SerializeToString,
                response_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.ReadinessResponse.FromString,
                )
        self.GetResource = channel.unary_unary(
                '/vdp.controller.v1beta.ControllerPrivateService/GetResource',
                request_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.GetResourceRequest.SerializeToString,
                response_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.GetResourceResponse.FromString,
                )
        self.UpdateResource = channel.unary_unary(
                '/vdp.controller.v1beta.ControllerPrivateService/UpdateResource',
                request_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.UpdateResourceRequest.SerializeToString,
                response_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.UpdateResourceResponse.FromString,
                )
        self.DeleteResource = channel.unary_unary(
                '/vdp.controller.v1beta.ControllerPrivateService/DeleteResource',
                request_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.DeleteResourceRequest.SerializeToString,
                response_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.DeleteResourceResponse.FromString,
                )


class ControllerPrivateServiceServicer(object):
    """Controller service responds to incoming controller requests
    """

    def Liveness(self, request, context):
        """Liveness method receives a LivenessRequest message and returns a
        LivenessResponse message.
        See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Readiness(self, request, context):
        """Readiness method receives a ReadinessRequest message and returns a
        ReadinessResponse message.
        See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetResource(self, request, context):
        """GetResource method receives a GetResourceRequest message
        and returns a GetResourceResponse
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateResource(self, request, context):
        """UpdateResource method receives a UpdateResourceRequest message
        and returns a UpdateResourceResponse
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteResource(self, request, context):
        """DeleteResource method receives a DeleteResourceRequest message
        and returns a DeleteResourceResponse
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ControllerPrivateServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Liveness': grpc.unary_unary_rpc_method_handler(
                    servicer.Liveness,
                    request_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.LivenessRequest.FromString,
                    response_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.LivenessResponse.SerializeToString,
            ),
            'Readiness': grpc.unary_unary_rpc_method_handler(
                    servicer.Readiness,
                    request_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.ReadinessRequest.FromString,
                    response_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.ReadinessResponse.SerializeToString,
            ),
            'GetResource': grpc.unary_unary_rpc_method_handler(
                    servicer.GetResource,
                    request_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.GetResourceRequest.FromString,
                    response_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.GetResourceResponse.SerializeToString,
            ),
            'UpdateResource': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateResource,
                    request_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.UpdateResourceRequest.FromString,
                    response_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.UpdateResourceResponse.SerializeToString,
            ),
            'DeleteResource': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteResource,
                    request_deserializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.DeleteResourceRequest.FromString,
                    response_serializer=vdp_dot_controller_dot_v1beta_dot_controller__pb2.DeleteResourceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'vdp.controller.v1beta.ControllerPrivateService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ControllerPrivateService(object):
    """Controller service responds to incoming controller requests
    """

    @staticmethod
    def Liveness(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/vdp.controller.v1beta.ControllerPrivateService/Liveness',
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.LivenessRequest.SerializeToString,
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.LivenessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Readiness(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/vdp.controller.v1beta.ControllerPrivateService/Readiness',
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.ReadinessRequest.SerializeToString,
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.ReadinessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetResource(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/vdp.controller.v1beta.ControllerPrivateService/GetResource',
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.GetResourceRequest.SerializeToString,
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.GetResourceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateResource(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/vdp.controller.v1beta.ControllerPrivateService/UpdateResource',
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.UpdateResourceRequest.SerializeToString,
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.UpdateResourceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteResource(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/vdp.controller.v1beta.ControllerPrivateService/DeleteResource',
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.DeleteResourceRequest.SerializeToString,
            vdp_dot_controller_dot_v1beta_dot_controller__pb2.DeleteResourceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
