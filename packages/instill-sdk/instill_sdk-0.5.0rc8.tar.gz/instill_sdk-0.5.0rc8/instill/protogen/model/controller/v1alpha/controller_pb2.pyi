"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import common.healthcheck.v1beta.healthcheck_pb2
import google.protobuf.descriptor
import google.protobuf.message
import model.model.v1alpha.model_pb2
import sys
import typing

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class LivenessRequest(google.protobuf.message.Message):
    """LivenessRequest represents a request to check a service liveness status"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEALTH_CHECK_REQUEST_FIELD_NUMBER: builtins.int
    @property
    def health_check_request(self) -> common.healthcheck.v1beta.healthcheck_pb2.HealthCheckRequest:
        """HealthCheckRequest message"""
    def __init__(
        self,
        *,
        health_check_request: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_health_check_request", b"_health_check_request", "health_check_request", b"health_check_request"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_health_check_request", b"_health_check_request", "health_check_request", b"health_check_request"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_health_check_request", b"_health_check_request"]) -> typing_extensions.Literal["health_check_request"] | None: ...

global___LivenessRequest = LivenessRequest

@typing_extensions.final
class LivenessResponse(google.protobuf.message.Message):
    """LivenessResponse represents a response for a service liveness status"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEALTH_CHECK_RESPONSE_FIELD_NUMBER: builtins.int
    @property
    def health_check_response(self) -> common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse:
        """HealthCheckResponse message"""
    def __init__(
        self,
        *,
        health_check_response: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["health_check_response", b"health_check_response"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["health_check_response", b"health_check_response"]) -> None: ...

global___LivenessResponse = LivenessResponse

@typing_extensions.final
class ReadinessRequest(google.protobuf.message.Message):
    """ReadinessRequest represents a request to check a service readiness status"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEALTH_CHECK_REQUEST_FIELD_NUMBER: builtins.int
    @property
    def health_check_request(self) -> common.healthcheck.v1beta.healthcheck_pb2.HealthCheckRequest:
        """HealthCheckRequest message"""
    def __init__(
        self,
        *,
        health_check_request: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_health_check_request", b"_health_check_request", "health_check_request", b"health_check_request"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_health_check_request", b"_health_check_request", "health_check_request", b"health_check_request"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_health_check_request", b"_health_check_request"]) -> typing_extensions.Literal["health_check_request"] | None: ...

global___ReadinessRequest = ReadinessRequest

@typing_extensions.final
class ReadinessResponse(google.protobuf.message.Message):
    """ReadinessResponse represents a response for a service readiness status"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEALTH_CHECK_RESPONSE_FIELD_NUMBER: builtins.int
    @property
    def health_check_response(self) -> common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse:
        """HealthCheckResponse message"""
    def __init__(
        self,
        *,
        health_check_response: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["health_check_response", b"health_check_response"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["health_check_response", b"health_check_response"]) -> None: ...

global___ReadinessResponse = ReadinessResponse

@typing_extensions.final
class Resource(google.protobuf.message.Message):
    """Resource represents the current information of a resource"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_PERMALINK_FIELD_NUMBER: builtins.int
    MODEL_STATE_FIELD_NUMBER: builtins.int
    BACKEND_STATE_FIELD_NUMBER: builtins.int
    PROGRESS_FIELD_NUMBER: builtins.int
    resource_permalink: builtins.str
    """Permalink of a resource. For example:
    "resources/{resource_uuid}/types/{type}"
    """
    model_state: model.model.v1alpha.model_pb2.Model.State.ValueType
    """Model state"""
    backend_state: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse.ServingStatus.ValueType
    """Backend service state"""
    progress: builtins.int
    """Resource longrunning progress"""
    def __init__(
        self,
        *,
        resource_permalink: builtins.str = ...,
        model_state: model.model.v1alpha.model_pb2.Model.State.ValueType = ...,
        backend_state: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse.ServingStatus.ValueType = ...,
        progress: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_progress", b"_progress", "backend_state", b"backend_state", "model_state", b"model_state", "progress", b"progress", "state", b"state"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_progress", b"_progress", "backend_state", b"backend_state", "model_state", b"model_state", "progress", b"progress", "resource_permalink", b"resource_permalink", "state", b"state"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_progress", b"_progress"]) -> typing_extensions.Literal["progress"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["state", b"state"]) -> typing_extensions.Literal["model_state", "backend_state"] | None: ...

global___Resource = Resource

@typing_extensions.final
class GetResourceRequest(google.protobuf.message.Message):
    """GetResourceRequest represents a request to query a resource's state"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_PERMALINK_FIELD_NUMBER: builtins.int
    resource_permalink: builtins.str
    """Permalink of a resource. For example:
    "resources/{resource_uuid}/types/{type}"
    """
    def __init__(
        self,
        *,
        resource_permalink: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource_permalink", b"resource_permalink"]) -> None: ...

global___GetResourceRequest = GetResourceRequest

@typing_extensions.final
class GetResourceResponse(google.protobuf.message.Message):
    """GetResourceResponse represents a response to fetch a resource's state"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_FIELD_NUMBER: builtins.int
    @property
    def resource(self) -> global___Resource:
        """Retrieved resource state"""
    def __init__(
        self,
        *,
        resource: global___Resource | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource", b"resource"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource", b"resource"]) -> None: ...

global___GetResourceResponse = GetResourceResponse

@typing_extensions.final
class UpdateResourceRequest(google.protobuf.message.Message):
    """UpdateResourceRequest represents a request to update a resource's state"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_FIELD_NUMBER: builtins.int
    WORKFLOW_ID_FIELD_NUMBER: builtins.int
    @property
    def resource(self) -> global___Resource:
        """Resource state"""
    workflow_id: builtins.str
    """Resource long-running workflow id"""
    def __init__(
        self,
        *,
        resource: global___Resource | None = ...,
        workflow_id: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_workflow_id", b"_workflow_id", "resource", b"resource", "workflow_id", b"workflow_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_workflow_id", b"_workflow_id", "resource", b"resource", "workflow_id", b"workflow_id"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_workflow_id", b"_workflow_id"]) -> typing_extensions.Literal["workflow_id"] | None: ...

global___UpdateResourceRequest = UpdateResourceRequest

@typing_extensions.final
class UpdateResourceResponse(google.protobuf.message.Message):
    """UpdateResourceResponse represents a response to update a resource's state"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_FIELD_NUMBER: builtins.int
    @property
    def resource(self) -> global___Resource:
        """Updated resource state"""
    def __init__(
        self,
        *,
        resource: global___Resource | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource", b"resource"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource", b"resource"]) -> None: ...

global___UpdateResourceResponse = UpdateResourceResponse

@typing_extensions.final
class DeleteResourceRequest(google.protobuf.message.Message):
    """DeleteResourceRequest represents a request to delete a resource's state"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_PERMALINK_FIELD_NUMBER: builtins.int
    resource_permalink: builtins.str
    """Permalink of a resource. For example:
    "resources/{resource_uuid}/types/{type}"
    """
    def __init__(
        self,
        *,
        resource_permalink: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["resource_permalink", b"resource_permalink"]) -> None: ...

global___DeleteResourceRequest = DeleteResourceRequest

@typing_extensions.final
class DeleteResourceResponse(google.protobuf.message.Message):
    """DeleteResourceResponse represents an empty response"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeleteResourceResponse = DeleteResourceResponse
