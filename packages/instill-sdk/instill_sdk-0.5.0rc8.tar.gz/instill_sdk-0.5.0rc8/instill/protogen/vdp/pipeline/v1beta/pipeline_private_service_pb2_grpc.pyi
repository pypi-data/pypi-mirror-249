"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import collections.abc
import grpc
import grpc.aio
import typing
import vdp.pipeline.v1beta.connector_definition_pb2
import vdp.pipeline.v1beta.connector_pb2
import vdp.pipeline.v1beta.operator_definition_pb2
import vdp.pipeline.v1beta.pipeline_pb2

_T = typing.TypeVar('_T')

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta):
    ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore
    ...

class PipelinePrivateServiceStub:
    """PipelinePrivateService defines private methods to interact with Pipeline
    resources.
    """

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    ListPipelinesAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.pipeline_pb2.ListPipelinesAdminRequest,
        vdp.pipeline.v1beta.pipeline_pb2.ListPipelinesAdminResponse,
    ]
    """List pipelines (admin only).

    This is a *private* method that allows admin users and internal clients to
    list *all* pipeline resources.
    """
    LookUpPipelineAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.pipeline_pb2.LookUpPipelineAdminRequest,
        vdp.pipeline.v1beta.pipeline_pb2.LookUpPipelineAdminResponse,
    ]
    """Get a pipeline by UID (admin only).

    This is a *private* method that allows admin users to access any pipeline
    resource by its UID.
    """
    LookUpOperatorDefinitionAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.operator_definition_pb2.LookUpOperatorDefinitionAdminRequest,
        vdp.pipeline.v1beta.operator_definition_pb2.LookUpOperatorDefinitionAdminResponse,
    ]
    """Get an operator definition by UID (admin only).

    This is a *private* method that allows admin users to access an operator
    definition by its UID.
    """
    ListPipelineReleasesAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.pipeline_pb2.ListPipelineReleasesAdminRequest,
        vdp.pipeline.v1beta.pipeline_pb2.ListPipelineReleasesAdminResponse,
    ]
    """List pipeline releases (admin only).

    This is a *private* method that allows admin users to list *all* pipeline
    releases.
    """
    LookUpConnectorDefinitionAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.connector_definition_pb2.LookUpConnectorDefinitionAdminRequest,
        vdp.pipeline.v1beta.connector_definition_pb2.LookUpConnectorDefinitionAdminResponse,
    ]
    """Get a connector definition by UID (admin only).

    This is a *private* method that allows admin users to access a connector
    definition by its UID.
    """
    ListConnectorsAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.connector_pb2.ListConnectorsAdminRequest,
        vdp.pipeline.v1beta.connector_pb2.ListConnectorsAdminResponse,
    ]
    """List connectors (admin only).

    This is a *private* method that allows admin users to list *all* connectors.
    """
    LookUpConnectorAdmin: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.connector_pb2.LookUpConnectorAdminRequest,
        vdp.pipeline.v1beta.connector_pb2.LookUpConnectorAdminResponse,
    ]
    """Get a connector by UID (admin only).

    This is a *private* method that allows admin users to access a connector
    by its UID.
    """
    CheckConnector: grpc.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.connector_pb2.CheckConnectorRequest,
        vdp.pipeline.v1beta.connector_pb2.CheckConnectorResponse,
    ]
    """Get a connector current state (admin only).

    This is a *private* method that allows admin users to access the state of
    a connector by its UID.
    """

class PipelinePrivateServiceAsyncStub:
    """PipelinePrivateService defines private methods to interact with Pipeline
    resources.
    """

    ListPipelinesAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.pipeline_pb2.ListPipelinesAdminRequest,
        vdp.pipeline.v1beta.pipeline_pb2.ListPipelinesAdminResponse,
    ]
    """List pipelines (admin only).

    This is a *private* method that allows admin users and internal clients to
    list *all* pipeline resources.
    """
    LookUpPipelineAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.pipeline_pb2.LookUpPipelineAdminRequest,
        vdp.pipeline.v1beta.pipeline_pb2.LookUpPipelineAdminResponse,
    ]
    """Get a pipeline by UID (admin only).

    This is a *private* method that allows admin users to access any pipeline
    resource by its UID.
    """
    LookUpOperatorDefinitionAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.operator_definition_pb2.LookUpOperatorDefinitionAdminRequest,
        vdp.pipeline.v1beta.operator_definition_pb2.LookUpOperatorDefinitionAdminResponse,
    ]
    """Get an operator definition by UID (admin only).

    This is a *private* method that allows admin users to access an operator
    definition by its UID.
    """
    ListPipelineReleasesAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.pipeline_pb2.ListPipelineReleasesAdminRequest,
        vdp.pipeline.v1beta.pipeline_pb2.ListPipelineReleasesAdminResponse,
    ]
    """List pipeline releases (admin only).

    This is a *private* method that allows admin users to list *all* pipeline
    releases.
    """
    LookUpConnectorDefinitionAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.connector_definition_pb2.LookUpConnectorDefinitionAdminRequest,
        vdp.pipeline.v1beta.connector_definition_pb2.LookUpConnectorDefinitionAdminResponse,
    ]
    """Get a connector definition by UID (admin only).

    This is a *private* method that allows admin users to access a connector
    definition by its UID.
    """
    ListConnectorsAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.connector_pb2.ListConnectorsAdminRequest,
        vdp.pipeline.v1beta.connector_pb2.ListConnectorsAdminResponse,
    ]
    """List connectors (admin only).

    This is a *private* method that allows admin users to list *all* connectors.
    """
    LookUpConnectorAdmin: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.connector_pb2.LookUpConnectorAdminRequest,
        vdp.pipeline.v1beta.connector_pb2.LookUpConnectorAdminResponse,
    ]
    """Get a connector by UID (admin only).

    This is a *private* method that allows admin users to access a connector
    by its UID.
    """
    CheckConnector: grpc.aio.UnaryUnaryMultiCallable[
        vdp.pipeline.v1beta.connector_pb2.CheckConnectorRequest,
        vdp.pipeline.v1beta.connector_pb2.CheckConnectorResponse,
    ]
    """Get a connector current state (admin only).

    This is a *private* method that allows admin users to access the state of
    a connector by its UID.
    """

class PipelinePrivateServiceServicer(metaclass=abc.ABCMeta):
    """PipelinePrivateService defines private methods to interact with Pipeline
    resources.
    """

    @abc.abstractmethod
    def ListPipelinesAdmin(
        self,
        request: vdp.pipeline.v1beta.pipeline_pb2.ListPipelinesAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1beta.pipeline_pb2.ListPipelinesAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1beta.pipeline_pb2.ListPipelinesAdminResponse]]:
        """List pipelines (admin only).

        This is a *private* method that allows admin users and internal clients to
        list *all* pipeline resources.
        """
    @abc.abstractmethod
    def LookUpPipelineAdmin(
        self,
        request: vdp.pipeline.v1beta.pipeline_pb2.LookUpPipelineAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1beta.pipeline_pb2.LookUpPipelineAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1beta.pipeline_pb2.LookUpPipelineAdminResponse]]:
        """Get a pipeline by UID (admin only).

        This is a *private* method that allows admin users to access any pipeline
        resource by its UID.
        """
    @abc.abstractmethod
    def LookUpOperatorDefinitionAdmin(
        self,
        request: vdp.pipeline.v1beta.operator_definition_pb2.LookUpOperatorDefinitionAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1beta.operator_definition_pb2.LookUpOperatorDefinitionAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1beta.operator_definition_pb2.LookUpOperatorDefinitionAdminResponse]]:
        """Get an operator definition by UID (admin only).

        This is a *private* method that allows admin users to access an operator
        definition by its UID.
        """
    @abc.abstractmethod
    def ListPipelineReleasesAdmin(
        self,
        request: vdp.pipeline.v1beta.pipeline_pb2.ListPipelineReleasesAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1beta.pipeline_pb2.ListPipelineReleasesAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1beta.pipeline_pb2.ListPipelineReleasesAdminResponse]]:
        """List pipeline releases (admin only).

        This is a *private* method that allows admin users to list *all* pipeline
        releases.
        """
    @abc.abstractmethod
    def LookUpConnectorDefinitionAdmin(
        self,
        request: vdp.pipeline.v1beta.connector_definition_pb2.LookUpConnectorDefinitionAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1beta.connector_definition_pb2.LookUpConnectorDefinitionAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1beta.connector_definition_pb2.LookUpConnectorDefinitionAdminResponse]]:
        """Get a connector definition by UID (admin only).

        This is a *private* method that allows admin users to access a connector
        definition by its UID.
        """
    @abc.abstractmethod
    def ListConnectorsAdmin(
        self,
        request: vdp.pipeline.v1beta.connector_pb2.ListConnectorsAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1beta.connector_pb2.ListConnectorsAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1beta.connector_pb2.ListConnectorsAdminResponse]]:
        """List connectors (admin only).

        This is a *private* method that allows admin users to list *all* connectors.
        """
    @abc.abstractmethod
    def LookUpConnectorAdmin(
        self,
        request: vdp.pipeline.v1beta.connector_pb2.LookUpConnectorAdminRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1beta.connector_pb2.LookUpConnectorAdminResponse, collections.abc.Awaitable[vdp.pipeline.v1beta.connector_pb2.LookUpConnectorAdminResponse]]:
        """Get a connector by UID (admin only).

        This is a *private* method that allows admin users to access a connector
        by its UID.
        """
    @abc.abstractmethod
    def CheckConnector(
        self,
        request: vdp.pipeline.v1beta.connector_pb2.CheckConnectorRequest,
        context: _ServicerContext,
    ) -> typing.Union[vdp.pipeline.v1beta.connector_pb2.CheckConnectorResponse, collections.abc.Awaitable[vdp.pipeline.v1beta.connector_pb2.CheckConnectorResponse]]:
        """Get a connector current state (admin only).

        This is a *private* method that allows admin users to access the state of
        a connector by its UID.
        """

def add_PipelinePrivateServiceServicer_to_server(servicer: PipelinePrivateServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
