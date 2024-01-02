# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: core/mgmt/v1beta/mgmt_public_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from core.mgmt.v1beta import metric_pb2 as core_dot_mgmt_dot_v1beta_dot_metric__pb2
from core.mgmt.v1beta import mgmt_pb2 as core_dot_mgmt_dot_v1beta_dot_mgmt__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import visibility_pb2 as google_dot_api_dot_visibility__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*core/mgmt/v1beta/mgmt_public_service.proto\x12\x10\x63ore.mgmt.v1beta\x1a\x1d\x63ore/mgmt/v1beta/metric.proto\x1a\x1b\x63ore/mgmt/v1beta/mgmt.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1bgoogle/api/visibility.proto2\xa6\x30\n\x11MgmtPublicService\x12\x84\x01\n\x08Liveness\x12!.core.mgmt.v1beta.LivenessRequest\x1a\".core.mgmt.v1beta.LivenessResponse\"1\x82\xd3\xe4\x93\x02+\x12\x12/v1beta/__livenessZ\x15\x12\x13/v1beta/health/mgmt\x12\x87\x01\n\tReadiness\x12\".core.mgmt.v1beta.ReadinessRequest\x1a#.core.mgmt.v1beta.ReadinessResponse\"1\x82\xd3\xe4\x93\x02+\x12\x13/v1beta/__readinessZ\x14\x12\x12/v1beta/ready/mgmt\x12\x93\x01\n\x0e\x43heckNamespace\x12\'.core.mgmt.v1beta.CheckNamespaceRequest\x1a(.core.mgmt.v1beta.CheckNamespaceResponse\".\xda\x41\tnamespace\x82\xd3\xe4\x93\x02\x1c\"\x17/v1beta/check-namespace:\x01*\x12k\n\tListUsers\x12\".core.mgmt.v1beta.ListUsersRequest\x1a#.core.mgmt.v1beta.ListUsersResponse\"\x15\x82\xd3\xe4\x93\x02\x0f\x12\r/v1beta/users\x12u\n\x07GetUser\x12 .core.mgmt.v1beta.GetUserRequest\x1a!.core.mgmt.v1beta.GetUserResponse\"%\xda\x41\x04name\x82\xd3\xe4\x93\x02\x18\x12\x16/v1beta/{name=users/*}\x12\xae\x01\n\x16PatchAuthenticatedUser\x12/.core.mgmt.v1beta.PatchAuthenticatedUserRequest\x1a\x30.core.mgmt.v1beta.PatchAuthenticatedUserResponse\"1\xda\x41\x10user,update_mask\x82\xd3\xe4\x93\x02\x18\x32\x10/v1beta/users/me:\x04user\x12\xa9\x01\n\x13ListUserMemberships\x12,.core.mgmt.v1beta.ListUserMembershipsRequest\x1a-.core.mgmt.v1beta.ListUserMembershipsResponse\"5\xda\x41\x06parent\x82\xd3\xe4\x93\x02&\x12$/v1beta/{parent=users/*}/memberships\x12\xa1\x01\n\x11GetUserMembership\x12*.core.mgmt.v1beta.GetUserMembershipRequest\x1a+.core.mgmt.v1beta.GetUserMembershipResponse\"3\xda\x41\x04name\x82\xd3\xe4\x93\x02&\x12$/v1beta/{name=users/*/memberships/*}\x12\xd3\x01\n\x14UpdateUserMembership\x12-.core.mgmt.v1beta.UpdateUserMembershipRequest\x1a..core.mgmt.v1beta.UpdateUserMembershipResponse\"\\\xda\x41\x16membership,update_mask\x82\xd3\xe4\x93\x02=\x1a//v1beta/{membership.name=users/*/memberships/*}:\nmembership\x12\xaa\x01\n\x14\x44\x65leteUserMembership\x12-.core.mgmt.v1beta.DeleteUserMembershipRequest\x1a..core.mgmt.v1beta.DeleteUserMembershipResponse\"3\xda\x41\x04name\x82\xd3\xe4\x93\x02&*$/v1beta/{name=users/*/memberships/*}\x12\x8b\x01\n\x11ListOrganizations\x12*.core.mgmt.v1beta.ListOrganizationsRequest\x1a+.core.mgmt.v1beta.ListOrganizationsResponse\"\x1d\x82\xd3\xe4\x93\x02\x17\x12\x15/v1beta/organizations\x12\xab\x01\n\x12\x43reateOrganization\x12+.core.mgmt.v1beta.CreateOrganizationRequest\x1a,.core.mgmt.v1beta.CreateOrganizationResponse\":\xda\x41\x0corganization\x82\xd3\xe4\x93\x02%\"\x15/v1beta/organizations:\x0corganization\x12\x95\x01\n\x0fGetOrganization\x12(.core.mgmt.v1beta.GetOrganizationRequest\x1a).core.mgmt.v1beta.GetOrganizationResponse\"-\xda\x41\x04name\x82\xd3\xe4\x93\x02 \x12\x1e/v1beta/{name=organizations/*}\x12\xcd\x01\n\x12UpdateOrganization\x12+.core.mgmt.v1beta.UpdateOrganizationRequest\x1a,.core.mgmt.v1beta.UpdateOrganizationResponse\"\\\xda\x41\x18organization,update_mask\x82\xd3\xe4\x93\x02;2+/v1beta/{organization.name=organizations/*}:\x0corganization\x12\x9e\x01\n\x12\x44\x65leteOrganization\x12+.core.mgmt.v1beta.DeleteOrganizationRequest\x1a,.core.mgmt.v1beta.DeleteOrganizationResponse\"-\xda\x41\x04name\x82\xd3\xe4\x93\x02 *\x1e/v1beta/{name=organizations/*}\x12\xc9\x01\n\x1bListOrganizationMemberships\x12\x34.core.mgmt.v1beta.ListOrganizationMembershipsRequest\x1a\x35.core.mgmt.v1beta.ListOrganizationMembershipsResponse\"=\xda\x41\x06parent\x82\xd3\xe4\x93\x02.\x12,/v1beta/{parent=organizations/*}/memberships\x12\xc1\x01\n\x19GetOrganizationMembership\x12\x32.core.mgmt.v1beta.GetOrganizationMembershipRequest\x1a\x33.core.mgmt.v1beta.GetOrganizationMembershipResponse\";\xda\x41\x04name\x82\xd3\xe4\x93\x02.\x12,/v1beta/{name=organizations/*/memberships/*}\x12\xf3\x01\n\x1cUpdateOrganizationMembership\x12\x35.core.mgmt.v1beta.UpdateOrganizationMembershipRequest\x1a\x36.core.mgmt.v1beta.UpdateOrganizationMembershipResponse\"d\xda\x41\x16membership,update_mask\x82\xd3\xe4\x93\x02\x45\x1a\x37/v1beta/{membership.name=organizations/*/memberships/*}:\nmembership\x12\xca\x01\n\x1c\x44\x65leteOrganizationMembership\x12\x35.core.mgmt.v1beta.DeleteOrganizationMembershipRequest\x1a\x36.core.mgmt.v1beta.DeleteOrganizationMembershipResponse\";\xda\x41\x04name\x82\xd3\xe4\x93\x02.*,/v1beta/{name=organizations/*/memberships/*}\x12\xaa\x01\n\x13GetUserSubscription\x12,.core.mgmt.v1beta.GetUserSubscriptionRequest\x1a-.core.mgmt.v1beta.GetUserSubscriptionResponse\"6\xda\x41\x06parent\x82\xd3\xe4\x93\x02\'\x12%/v1beta/{parent=users/*}/subscription\x12\xca\x01\n\x1bGetOrganizationSubscription\x12\x34.core.mgmt.v1beta.GetOrganizationSubscriptionRequest\x1a\x35.core.mgmt.v1beta.GetOrganizationSubscriptionResponse\">\xda\x41\x06parent\x82\xd3\xe4\x93\x02/\x12-/v1beta/{parent=organizations/*}/subscription\x12\x81\x01\n\x0b\x43reateToken\x12$.core.mgmt.v1beta.CreateTokenRequest\x1a%.core.mgmt.v1beta.CreateTokenResponse\"%\xda\x41\x05token\x82\xd3\xe4\x93\x02\x17\"\x0e/v1beta/tokens:\x05token\x12o\n\nListTokens\x12#.core.mgmt.v1beta.ListTokensRequest\x1a$.core.mgmt.v1beta.ListTokensResponse\"\x16\x82\xd3\xe4\x93\x02\x10\x12\x0e/v1beta/tokens\x12y\n\x08GetToken\x12!.core.mgmt.v1beta.GetTokenRequest\x1a\".core.mgmt.v1beta.GetTokenResponse\"&\xda\x41\x04name\x82\xd3\xe4\x93\x02\x19\x12\x17/v1beta/{name=tokens/*}\x12\x82\x01\n\x0b\x44\x65leteToken\x12$.core.mgmt.v1beta.DeleteTokenRequest\x1a%.core.mgmt.v1beta.DeleteTokenResponse\"&\xda\x41\x04name\x82\xd3\xe4\x93\x02\x19*\x17/v1beta/{name=tokens/*}\x12\x80\x01\n\rValidateToken\x12&.core.mgmt.v1beta.ValidateTokenRequest\x1a\'.core.mgmt.v1beta.ValidateTokenResponse\"\x1e\x82\xd3\xe4\x93\x02\x18\"\x16/v1beta/validate_token\x12\xb6\x01\n\x1aListPipelineTriggerRecords\x12\x33.core.mgmt.v1beta.ListPipelineTriggerRecordsRequest\x1a\x34.core.mgmt.v1beta.ListPipelineTriggerRecordsResponse\"-\x82\xd3\xe4\x93\x02\'\x12%/v1beta/metrics/vdp/pipeline/triggers\x12\xc3\x01\n\x1fListPipelineTriggerTableRecords\x12\x38.core.mgmt.v1beta.ListPipelineTriggerTableRecordsRequest\x1a\x39.core.mgmt.v1beta.ListPipelineTriggerTableRecordsResponse\"+\x82\xd3\xe4\x93\x02%\x12#/v1beta/metrics/vdp/pipeline/tables\x12\xc3\x01\n\x1fListPipelineTriggerChartRecords\x12\x38.core.mgmt.v1beta.ListPipelineTriggerChartRecordsRequest\x1a\x39.core.mgmt.v1beta.ListPipelineTriggerChartRecordsResponse\"+\x82\xd3\xe4\x93\x02%\x12#/v1beta/metrics/vdp/pipeline/charts\x12\xba\x01\n\x1bListConnectorExecuteRecords\x12\x34.core.mgmt.v1beta.ListConnectorExecuteRecordsRequest\x1a\x35.core.mgmt.v1beta.ListConnectorExecuteRecordsResponse\".\x82\xd3\xe4\x93\x02(\x12&/v1beta/metrics/vdp/connector/executes\x12\xc7\x01\n ListConnectorExecuteTableRecords\x12\x39.core.mgmt.v1beta.ListConnectorExecuteTableRecordsRequest\x1a:.core.mgmt.v1beta.ListConnectorExecuteTableRecordsResponse\",\x82\xd3\xe4\x93\x02&\x12$/v1beta/metrics/vdp/connector/tables\x12\xc7\x01\n ListConnectorExecuteChartRecords\x12\x39.core.mgmt.v1beta.ListConnectorExecuteChartRecordsRequest\x1a:.core.mgmt.v1beta.ListConnectorExecuteChartRecordsResponse\",\x82\xd3\xe4\x93\x02&\x12$/v1beta/metrics/vdp/connector/charts\x12\x8c\x01\n\x0f\x41uthTokenIssuer\x12(.core.mgmt.v1beta.AuthTokenIssuerRequest\x1a).core.mgmt.v1beta.AuthTokenIssuerResponse\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/v1beta/auth/token_issuer:\x01*\x12p\n\tAuthLogin\x12\".core.mgmt.v1beta.AuthLoginRequest\x1a#.core.mgmt.v1beta.AuthLoginResponse\"\x1a\x82\xd3\xe4\x93\x02\x14\"\x12/v1beta/auth/login\x12t\n\nAuthLogout\x12#.core.mgmt.v1beta.AuthLogoutRequest\x1a$.core.mgmt.v1beta.AuthLogoutResponse\"\x1b\x82\xd3\xe4\x93\x02\x15\"\x13/v1beta/auth/logout\x12\x98\x01\n\x12\x41uthChangePassword\x12+.core.mgmt.v1beta.AuthChangePasswordRequest\x1a,.core.mgmt.v1beta.AuthChangePasswordResponse\"\'\x82\xd3\xe4\x93\x02!\"\x1c/v1beta/auth/change_password:\x01*\x12\xaa\x01\n\x17\x41uthValidateAccessToken\x12\x30.core.mgmt.v1beta.AuthValidateAccessTokenRequest\x1a\x31.core.mgmt.v1beta.AuthValidateAccessTokenResponse\"*\x82\xd3\xe4\x93\x02$\"\"/v1beta/auth/validate_access_token\x1a#\xca\x41\x10\x61pi.instill.tech\xfa\xd2\xe4\x93\x02\n\x12\x08INTERNALB\xcf\x01\n\x14\x63om.core.mgmt.v1betaB\x16MgmtPublicServiceProtoP\x01Z=github.com/instill-ai/protogen-go/core/mgmt/v1beta;mgmtv1beta\xa2\x02\x03\x43MX\xaa\x02\x10\x43ore.Mgmt.V1beta\xca\x02\x10\x43ore\\Mgmt\\V1beta\xe2\x02\x1c\x43ore\\Mgmt\\V1beta\\GPBMetadata\xea\x02\x12\x43ore::Mgmt::V1betab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'core.mgmt.v1beta.mgmt_public_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024com.core.mgmt.v1betaB\026MgmtPublicServiceProtoP\001Z=github.com/instill-ai/protogen-go/core/mgmt/v1beta;mgmtv1beta\242\002\003CMX\252\002\020Core.Mgmt.V1beta\312\002\020Core\\Mgmt\\V1beta\342\002\034Core\\Mgmt\\V1beta\\GPBMetadata\352\002\022Core::Mgmt::V1beta'
  _MGMTPUBLICSERVICE._options = None
  _MGMTPUBLICSERVICE._serialized_options = b'\312A\020api.instill.tech\372\322\344\223\002\n\022\010INTERNAL'
  _MGMTPUBLICSERVICE.methods_by_name['Liveness']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['Liveness']._serialized_options = b'\202\323\344\223\002+\022\022/v1beta/__livenessZ\025\022\023/v1beta/health/mgmt'
  _MGMTPUBLICSERVICE.methods_by_name['Readiness']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['Readiness']._serialized_options = b'\202\323\344\223\002+\022\023/v1beta/__readinessZ\024\022\022/v1beta/ready/mgmt'
  _MGMTPUBLICSERVICE.methods_by_name['CheckNamespace']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['CheckNamespace']._serialized_options = b'\332A\tnamespace\202\323\344\223\002\034\"\027/v1beta/check-namespace:\001*'
  _MGMTPUBLICSERVICE.methods_by_name['ListUsers']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListUsers']._serialized_options = b'\202\323\344\223\002\017\022\r/v1beta/users'
  _MGMTPUBLICSERVICE.methods_by_name['GetUser']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['GetUser']._serialized_options = b'\332A\004name\202\323\344\223\002\030\022\026/v1beta/{name=users/*}'
  _MGMTPUBLICSERVICE.methods_by_name['PatchAuthenticatedUser']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['PatchAuthenticatedUser']._serialized_options = b'\332A\020user,update_mask\202\323\344\223\002\0302\020/v1beta/users/me:\004user'
  _MGMTPUBLICSERVICE.methods_by_name['ListUserMemberships']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListUserMemberships']._serialized_options = b'\332A\006parent\202\323\344\223\002&\022$/v1beta/{parent=users/*}/memberships'
  _MGMTPUBLICSERVICE.methods_by_name['GetUserMembership']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['GetUserMembership']._serialized_options = b'\332A\004name\202\323\344\223\002&\022$/v1beta/{name=users/*/memberships/*}'
  _MGMTPUBLICSERVICE.methods_by_name['UpdateUserMembership']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['UpdateUserMembership']._serialized_options = b'\332A\026membership,update_mask\202\323\344\223\002=\032//v1beta/{membership.name=users/*/memberships/*}:\nmembership'
  _MGMTPUBLICSERVICE.methods_by_name['DeleteUserMembership']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['DeleteUserMembership']._serialized_options = b'\332A\004name\202\323\344\223\002&*$/v1beta/{name=users/*/memberships/*}'
  _MGMTPUBLICSERVICE.methods_by_name['ListOrganizations']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListOrganizations']._serialized_options = b'\202\323\344\223\002\027\022\025/v1beta/organizations'
  _MGMTPUBLICSERVICE.methods_by_name['CreateOrganization']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['CreateOrganization']._serialized_options = b'\332A\014organization\202\323\344\223\002%\"\025/v1beta/organizations:\014organization'
  _MGMTPUBLICSERVICE.methods_by_name['GetOrganization']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['GetOrganization']._serialized_options = b'\332A\004name\202\323\344\223\002 \022\036/v1beta/{name=organizations/*}'
  _MGMTPUBLICSERVICE.methods_by_name['UpdateOrganization']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['UpdateOrganization']._serialized_options = b'\332A\030organization,update_mask\202\323\344\223\002;2+/v1beta/{organization.name=organizations/*}:\014organization'
  _MGMTPUBLICSERVICE.methods_by_name['DeleteOrganization']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['DeleteOrganization']._serialized_options = b'\332A\004name\202\323\344\223\002 *\036/v1beta/{name=organizations/*}'
  _MGMTPUBLICSERVICE.methods_by_name['ListOrganizationMemberships']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListOrganizationMemberships']._serialized_options = b'\332A\006parent\202\323\344\223\002.\022,/v1beta/{parent=organizations/*}/memberships'
  _MGMTPUBLICSERVICE.methods_by_name['GetOrganizationMembership']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['GetOrganizationMembership']._serialized_options = b'\332A\004name\202\323\344\223\002.\022,/v1beta/{name=organizations/*/memberships/*}'
  _MGMTPUBLICSERVICE.methods_by_name['UpdateOrganizationMembership']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['UpdateOrganizationMembership']._serialized_options = b'\332A\026membership,update_mask\202\323\344\223\002E\0327/v1beta/{membership.name=organizations/*/memberships/*}:\nmembership'
  _MGMTPUBLICSERVICE.methods_by_name['DeleteOrganizationMembership']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['DeleteOrganizationMembership']._serialized_options = b'\332A\004name\202\323\344\223\002.*,/v1beta/{name=organizations/*/memberships/*}'
  _MGMTPUBLICSERVICE.methods_by_name['GetUserSubscription']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['GetUserSubscription']._serialized_options = b'\332A\006parent\202\323\344\223\002\'\022%/v1beta/{parent=users/*}/subscription'
  _MGMTPUBLICSERVICE.methods_by_name['GetOrganizationSubscription']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['GetOrganizationSubscription']._serialized_options = b'\332A\006parent\202\323\344\223\002/\022-/v1beta/{parent=organizations/*}/subscription'
  _MGMTPUBLICSERVICE.methods_by_name['CreateToken']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['CreateToken']._serialized_options = b'\332A\005token\202\323\344\223\002\027\"\016/v1beta/tokens:\005token'
  _MGMTPUBLICSERVICE.methods_by_name['ListTokens']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListTokens']._serialized_options = b'\202\323\344\223\002\020\022\016/v1beta/tokens'
  _MGMTPUBLICSERVICE.methods_by_name['GetToken']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['GetToken']._serialized_options = b'\332A\004name\202\323\344\223\002\031\022\027/v1beta/{name=tokens/*}'
  _MGMTPUBLICSERVICE.methods_by_name['DeleteToken']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['DeleteToken']._serialized_options = b'\332A\004name\202\323\344\223\002\031*\027/v1beta/{name=tokens/*}'
  _MGMTPUBLICSERVICE.methods_by_name['ValidateToken']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ValidateToken']._serialized_options = b'\202\323\344\223\002\030\"\026/v1beta/validate_token'
  _MGMTPUBLICSERVICE.methods_by_name['ListPipelineTriggerRecords']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListPipelineTriggerRecords']._serialized_options = b'\202\323\344\223\002\'\022%/v1beta/metrics/vdp/pipeline/triggers'
  _MGMTPUBLICSERVICE.methods_by_name['ListPipelineTriggerTableRecords']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListPipelineTriggerTableRecords']._serialized_options = b'\202\323\344\223\002%\022#/v1beta/metrics/vdp/pipeline/tables'
  _MGMTPUBLICSERVICE.methods_by_name['ListPipelineTriggerChartRecords']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListPipelineTriggerChartRecords']._serialized_options = b'\202\323\344\223\002%\022#/v1beta/metrics/vdp/pipeline/charts'
  _MGMTPUBLICSERVICE.methods_by_name['ListConnectorExecuteRecords']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListConnectorExecuteRecords']._serialized_options = b'\202\323\344\223\002(\022&/v1beta/metrics/vdp/connector/executes'
  _MGMTPUBLICSERVICE.methods_by_name['ListConnectorExecuteTableRecords']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListConnectorExecuteTableRecords']._serialized_options = b'\202\323\344\223\002&\022$/v1beta/metrics/vdp/connector/tables'
  _MGMTPUBLICSERVICE.methods_by_name['ListConnectorExecuteChartRecords']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['ListConnectorExecuteChartRecords']._serialized_options = b'\202\323\344\223\002&\022$/v1beta/metrics/vdp/connector/charts'
  _MGMTPUBLICSERVICE.methods_by_name['AuthTokenIssuer']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['AuthTokenIssuer']._serialized_options = b'\202\323\344\223\002\036\"\031/v1beta/auth/token_issuer:\001*'
  _MGMTPUBLICSERVICE.methods_by_name['AuthLogin']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['AuthLogin']._serialized_options = b'\202\323\344\223\002\024\"\022/v1beta/auth/login'
  _MGMTPUBLICSERVICE.methods_by_name['AuthLogout']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['AuthLogout']._serialized_options = b'\202\323\344\223\002\025\"\023/v1beta/auth/logout'
  _MGMTPUBLICSERVICE.methods_by_name['AuthChangePassword']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['AuthChangePassword']._serialized_options = b'\202\323\344\223\002!\"\034/v1beta/auth/change_password:\001*'
  _MGMTPUBLICSERVICE.methods_by_name['AuthValidateAccessToken']._options = None
  _MGMTPUBLICSERVICE.methods_by_name['AuthValidateAccessToken']._serialized_options = b'\202\323\344\223\002$\"\"/v1beta/auth/validate_access_token'
  _globals['_MGMTPUBLICSERVICE']._serialized_start=209
  _globals['_MGMTPUBLICSERVICE']._serialized_end=6391
# @@protoc_insertion_point(module_scope)
