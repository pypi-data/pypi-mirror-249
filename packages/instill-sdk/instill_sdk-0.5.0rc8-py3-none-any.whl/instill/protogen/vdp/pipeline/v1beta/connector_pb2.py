# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vdp/pipeline/v1beta/connector.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
from vdp.pipeline.v1beta import connector_definition_pb2 as vdp_dot_pipeline_dot_v1beta_dot_connector__definition__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#vdp/pipeline/v1beta/connector.proto\x12\x13vdp.pipeline.v1beta\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a google/protobuf/field_mask.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a.protoc-gen-openapiv2/options/annotations.proto\x1a.vdp/pipeline/v1beta/connector_definition.proto\"\x8b\n\n\tConnector\x12\x18\n\x04name\x18\x01 \x01(\tB\x04\xe2\x41\x01\x03R\x04name\x12\x16\n\x03uid\x18\x02 \x01(\tB\x04\xe2\x41\x01\x03R\x03uid\x12\x14\n\x02id\x18\x03 \x01(\tB\x04\xe2\x41\x01\x05R\x02id\x12i\n\x19\x63onnector_definition_name\x18\x04 \x01(\tB-\xe2\x41\x01\x05\xfa\x41&\n$api.instill.tech/ConnectorDefinitionR\x17\x63onnectorDefinitionName\x12<\n\x04type\x18\x05 \x01(\x0e\x32\".vdp.pipeline.v1beta.ConnectorTypeB\x04\xe2\x41\x01\x03R\x04type\x12+\n\x0b\x64\x65scription\x18\x07 \x01(\tB\x04\xe2\x41\x01\x01H\x00R\x0b\x64\x65scription\x88\x01\x01\x12\x43\n\rconfiguration\x18\x08 \x01(\x0b\x32\x17.google.protobuf.StructB\x04\xe2\x41\x01\x02R\rconfiguration\x12@\n\x05state\x18\t \x01(\x0e\x32$.vdp.pipeline.v1beta.Connector.StateB\x04\xe2\x41\x01\x03R\x05state\x12\"\n\ttombstone\x18\n \x01(\x08\x42\x04\xe2\x41\x01\x03R\ttombstone\x12\x41\n\x0b\x63reate_time\x18\r \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\xe2\x41\x01\x03R\ncreateTime\x12\x41\n\x0bupdate_time\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\xe2\x41\x01\x03R\nupdateTime\x12O\n\nvisibility\x18\x0f \x01(\x0e\x32).vdp.pipeline.v1beta.Connector.VisibilityB\x04\xe2\x41\x01\x03R\nvisibility\x12\x61\n\x14\x63onnector_definition\x18\x10 \x01(\x0b\x32(.vdp.pipeline.v1beta.ConnectorDefinitionB\x04\xe2\x41\x01\x03R\x13\x63onnectorDefinition\x12\x41\n\x0b\x64\x65lete_time\x18\x11 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\xe2\x41\x01\x03R\ndeleteTime\x12#\n\nowner_name\x18\x12 \x01(\tB\x04\xe2\x41\x01\x03R\townerName\x12\x33\n\x05owner\x18\x13 \x01(\x0b\x32\x17.google.protobuf.StructB\x04\xe2\x41\x01\x03R\x05owner\"S\n\x04View\x12\x14\n\x10VIEW_UNSPECIFIED\x10\x00\x12\x0e\n\nVIEW_BASIC\x10\x01\x12\r\n\tVIEW_FULL\x10\x02\x12\x16\n\x12VIEW_CONFIGURATION\x10\x03\"\\\n\x05State\x12\x15\n\x11STATE_UNSPECIFIED\x10\x00\x12\x16\n\x12STATE_DISCONNECTED\x10\x01\x12\x13\n\x0fSTATE_CONNECTED\x10\x02\x12\x0f\n\x0bSTATE_ERROR\x10\x03\"W\n\nVisibility\x12\x1a\n\x16VISIBILITY_UNSPECIFIED\x10\x00\x12\x16\n\x12VISIBILITY_PRIVATE\x10\x01\x12\x15\n\x11VISIBILITY_PUBLIC\x10\x02:B\xea\x41?\n\x1a\x61pi.instill.tech/Connector\x12\x0f\x63onnectors/{id}\x12\x10\x63onnectors/{uid}B\x0e\n\x0c_description\"\xc0\x02\n\x15ListConnectorsRequest\x12&\n\tpage_size\x18\x01 \x01(\x05\x42\x04\xe2\x41\x01\x01H\x00R\x08pageSize\x88\x01\x01\x12(\n\npage_token\x18\x02 \x01(\tB\x04\xe2\x41\x01\x01H\x01R\tpageToken\x88\x01\x01\x12\x42\n\x04view\x18\x03 \x01(\x0e\x32#.vdp.pipeline.v1beta.Connector.ViewB\x04\xe2\x41\x01\x01H\x02R\x04view\x88\x01\x01\x12!\n\x06\x66ilter\x18\x04 \x01(\tB\x04\xe2\x41\x01\x01H\x03R\x06\x66ilter\x88\x01\x01\x12,\n\x0cshow_deleted\x18\x05 \x01(\x08\x42\x04\xe2\x41\x01\x01H\x04R\x0bshowDeleted\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\x07\n\x05_viewB\t\n\x07_filterB\x0f\n\r_show_deleted\"\x9f\x01\n\x16ListConnectorsResponse\x12>\n\nconnectors\x18\x01 \x03(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\nconnectors\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\x12\x1d\n\ntotal_size\x18\x03 \x01(\x05R\ttotalSize\"\xce\x01\n\x16LookUpConnectorRequest\x12g\n\tpermalink\x18\x01 \x01(\tBI\x92\x41#\xca> \xfa\x02\x1doperator_definition.permalink\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\tpermalink\x12\x42\n\x04view\x18\x02 \x01(\x0e\x32#.vdp.pipeline.v1beta.Connector.ViewB\x04\xe2\x41\x01\x01H\x00R\x04view\x88\x01\x01\x42\x07\n\x05_view\"W\n\x17LookUpConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"\x9d\x01\n\x1a\x43reateUserConnectorRequest\x12\x42\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorB\x04\xe2\x41\x01\x02R\tconnector\x12;\n\x06parent\x18\x02 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\x12\x1a\x61pi.instill.tech/ConnectorR\x06parent\"[\n\x1b\x43reateUserConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"\x81\x03\n\x19ListUserConnectorsRequest\x12&\n\tpage_size\x18\x01 \x01(\x05\x42\x04\xe2\x41\x01\x01H\x00R\x08pageSize\x88\x01\x01\x12(\n\npage_token\x18\x02 \x01(\tB\x04\xe2\x41\x01\x01H\x01R\tpageToken\x88\x01\x01\x12\x42\n\x04view\x18\x03 \x01(\x0e\x32#.vdp.pipeline.v1beta.Connector.ViewB\x04\xe2\x41\x01\x01H\x02R\x04view\x88\x01\x01\x12!\n\x06\x66ilter\x18\x04 \x01(\tB\x04\xe2\x41\x01\x01H\x03R\x06\x66ilter\x88\x01\x01\x12;\n\x06parent\x18\x05 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\x12\x1a\x61pi.instill.tech/ConnectorR\x06parent\x12,\n\x0cshow_deleted\x18\x06 \x01(\x08\x42\x04\xe2\x41\x01\x01H\x04R\x0bshowDeleted\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\x07\n\x05_viewB\t\n\x07_filterB\x0f\n\r_show_deleted\"\xa3\x01\n\x1aListUserConnectorsResponse\x12>\n\nconnectors\x18\x01 \x03(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\nconnectors\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\x12\x1d\n\ntotal_size\x18\x03 \x01(\x05R\ttotalSize\"\xb6\x01\n\x17GetUserConnectorRequest\x12N\n\x04name\x18\x01 \x01(\tB:\x92\x41\x14\xca>\x11\xfa\x02\x0e\x63onnector.name\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\x12\x42\n\x04view\x18\x03 \x01(\x0e\x32#.vdp.pipeline.v1beta.Connector.ViewB\x04\xe2\x41\x01\x01H\x00R\x04view\x88\x01\x01\x42\x07\n\x05_view\"X\n\x18GetUserConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"\xa3\x01\n\x1aUpdateUserConnectorRequest\x12\x42\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorB\x04\xe2\x41\x01\x02R\tconnector\x12\x41\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskB\x04\xe2\x41\x01\x02R\nupdateMask\"[\n\x1bUpdateUserConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"l\n\x1a\x44\x65leteUserConnectorRequest\x12N\n\x04name\x18\x01 \x01(\tB:\x92\x41\x14\xca>\x11\xfa\x02\x0e\x63onnector.name\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"\x1d\n\x1b\x44\x65leteUserConnectorResponse\"V\n\x1b\x43onnectUserConnectorRequest\x12\x37\n\x04name\x18\x01 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"\\\n\x1c\x43onnectUserConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"Y\n\x1e\x44isconnectUserConnectorRequest\x12\x37\n\x04name\x18\x01 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"_\n\x1f\x44isconnectUserConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"\x85\x01\n\x1aRenameUserConnectorRequest\x12\x37\n\x04name\x18\x01 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\x12.\n\x10new_connector_id\x18\x02 \x01(\tB\x04\xe2\x41\x01\x02R\x0enewConnectorId\"[\n\x1bRenameUserConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"|\n\x1b\x45xecuteUserConnectorRequest\x12\x18\n\x04name\x18\x01 \x01(\tB\x04\xe2\x41\x01\x02R\x04name\x12/\n\x06inputs\x18\x02 \x03(\x0b\x32\x17.google.protobuf.StructR\x06inputs\x12\x12\n\x04task\x18\x03 \x01(\tR\x04task\"Q\n\x1c\x45xecuteUserConnectorResponse\x12\x31\n\x07outputs\x18\x01 \x03(\x0b\x32\x17.google.protobuf.StructR\x07outputs\"j\n\x18TestUserConnectorRequest\x12N\n\x04name\x18\x01 \x01(\tB:\x92\x41\x14\xca>\x11\xfa\x02\x0e\x63onnector.name\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"W\n\x19TestUserConnectorResponse\x12:\n\x05state\x18\x01 \x01(\x0e\x32$.vdp.pipeline.v1beta.Connector.StateR\x05state\"k\n\x19WatchUserConnectorRequest\x12N\n\x04name\x18\x01 \x01(\tB:\x92\x41\x14\xca>\x11\xfa\x02\x0e\x63onnector.name\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"X\n\x1aWatchUserConnectorResponse\x12:\n\x05state\x18\x01 \x01(\x0e\x32$.vdp.pipeline.v1beta.Connector.StateR\x05state\"\xa5\x01\n\"CreateOrganizationConnectorRequest\x12\x42\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorB\x04\xe2\x41\x01\x02R\tconnector\x12;\n\x06parent\x18\x02 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\x12\x1a\x61pi.instill.tech/ConnectorR\x06parent\"c\n#CreateOrganizationConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"\x89\x03\n!ListOrganizationConnectorsRequest\x12&\n\tpage_size\x18\x01 \x01(\x05\x42\x04\xe2\x41\x01\x01H\x00R\x08pageSize\x88\x01\x01\x12(\n\npage_token\x18\x02 \x01(\tB\x04\xe2\x41\x01\x01H\x01R\tpageToken\x88\x01\x01\x12\x42\n\x04view\x18\x03 \x01(\x0e\x32#.vdp.pipeline.v1beta.Connector.ViewB\x04\xe2\x41\x01\x01H\x02R\x04view\x88\x01\x01\x12!\n\x06\x66ilter\x18\x04 \x01(\tB\x04\xe2\x41\x01\x01H\x03R\x06\x66ilter\x88\x01\x01\x12;\n\x06parent\x18\x05 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\x12\x1a\x61pi.instill.tech/ConnectorR\x06parent\x12,\n\x0cshow_deleted\x18\x06 \x01(\x08\x42\x04\xe2\x41\x01\x01H\x04R\x0bshowDeleted\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\x07\n\x05_viewB\t\n\x07_filterB\x0f\n\r_show_deleted\"\xab\x01\n\"ListOrganizationConnectorsResponse\x12>\n\nconnectors\x18\x01 \x03(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\nconnectors\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\x12\x1d\n\ntotal_size\x18\x03 \x01(\x05R\ttotalSize\"\xbe\x01\n\x1fGetOrganizationConnectorRequest\x12N\n\x04name\x18\x01 \x01(\tB:\x92\x41\x14\xca>\x11\xfa\x02\x0e\x63onnector.name\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\x12\x42\n\x04view\x18\x03 \x01(\x0e\x32#.vdp.pipeline.v1beta.Connector.ViewB\x04\xe2\x41\x01\x01H\x00R\x04view\x88\x01\x01\x42\x07\n\x05_view\"`\n GetOrganizationConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"\xab\x01\n\"UpdateOrganizationConnectorRequest\x12\x42\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorB\x04\xe2\x41\x01\x02R\tconnector\x12\x41\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskB\x04\xe2\x41\x01\x02R\nupdateMask\"c\n#UpdateOrganizationConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"t\n\"DeleteOrganizationConnectorRequest\x12N\n\x04name\x18\x01 \x01(\tB:\x92\x41\x14\xca>\x11\xfa\x02\x0e\x63onnector.name\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"%\n#DeleteOrganizationConnectorResponse\"^\n#ConnectOrganizationConnectorRequest\x12\x37\n\x04name\x18\x01 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"d\n$ConnectOrganizationConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"a\n&DisconnectOrganizationConnectorRequest\x12\x37\n\x04name\x18\x01 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"g\n\'DisconnectOrganizationConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"\x8d\x01\n\"RenameOrganizationConnectorRequest\x12\x37\n\x04name\x18\x01 \x01(\tB#\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\x12.\n\x10new_connector_id\x18\x02 \x01(\tB\x04\xe2\x41\x01\x02R\x0enewConnectorId\"c\n#RenameOrganizationConnectorResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\"\x84\x01\n#ExecuteOrganizationConnectorRequest\x12\x18\n\x04name\x18\x01 \x01(\tB\x04\xe2\x41\x01\x02R\x04name\x12/\n\x06inputs\x18\x02 \x03(\x0b\x32\x17.google.protobuf.StructR\x06inputs\x12\x12\n\x04task\x18\x03 \x01(\tR\x04task\"Y\n$ExecuteOrganizationConnectorResponse\x12\x31\n\x07outputs\x18\x01 \x03(\x0b\x32\x17.google.protobuf.StructR\x07outputs\"r\n TestOrganizationConnectorRequest\x12N\n\x04name\x18\x01 \x01(\tB:\x92\x41\x14\xca>\x11\xfa\x02\x0e\x63onnector.name\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"_\n!TestOrganizationConnectorResponse\x12:\n\x05state\x18\x01 \x01(\x0e\x32$.vdp.pipeline.v1beta.Connector.StateR\x05state\"s\n!WatchOrganizationConnectorRequest\x12N\n\x04name\x18\x01 \x01(\tB:\x92\x41\x14\xca>\x11\xfa\x02\x0e\x63onnector.name\xe2\x41\x01\x02\xfa\x41\x1c\n\x1a\x61pi.instill.tech/ConnectorR\x04name\"`\n\"WatchOrganizationConnectorResponse\x12:\n\x05state\x18\x01 \x01(\x0e\x32$.vdp.pipeline.v1beta.Connector.StateR\x05state\"\xc5\x02\n\x1aListConnectorsAdminRequest\x12&\n\tpage_size\x18\x01 \x01(\x05\x42\x04\xe2\x41\x01\x01H\x00R\x08pageSize\x88\x01\x01\x12(\n\npage_token\x18\x02 \x01(\tB\x04\xe2\x41\x01\x01H\x01R\tpageToken\x88\x01\x01\x12\x42\n\x04view\x18\x03 \x01(\x0e\x32#.vdp.pipeline.v1beta.Connector.ViewB\x04\xe2\x41\x01\x01H\x02R\x04view\x88\x01\x01\x12!\n\x06\x66ilter\x18\x04 \x01(\tB\x04\xe2\x41\x01\x01H\x03R\x06\x66ilter\x88\x01\x01\x12,\n\x0cshow_deleted\x18\x05 \x01(\x08\x42\x04\xe2\x41\x01\x01H\x04R\x0bshowDeleted\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\x07\n\x05_viewB\t\n\x07_filterB\x0f\n\r_show_deleted\"\xa4\x01\n\x1bListConnectorsAdminResponse\x12>\n\nconnectors\x18\x01 \x03(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\nconnectors\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\x12\x1d\n\ntotal_size\x18\x03 \x01(\x05R\ttotalSize\"\x8e\x01\n\x1bLookUpConnectorAdminRequest\x12\"\n\tpermalink\x18\x01 \x01(\tB\x04\xe2\x41\x01\x02R\tpermalink\x12\x42\n\x04view\x18\x02 \x01(\x0e\x32#.vdp.pipeline.v1beta.Connector.ViewB\x04\xe2\x41\x01\x01H\x00R\x04view\x88\x01\x01\x42\x07\n\x05_view\"\\\n\x1cLookUpConnectorAdminResponse\x12<\n\tconnector\x18\x01 \x01(\x0b\x32\x1e.vdp.pipeline.v1beta.ConnectorR\tconnector\";\n\x15\x43heckConnectorRequest\x12\"\n\tpermalink\x18\x01 \x01(\tB\x04\xe2\x41\x01\x02R\tpermalink\"T\n\x16\x43heckConnectorResponse\x12:\n\x05state\x18\x01 \x01(\x0e\x32$.vdp.pipeline.v1beta.Connector.StateR\x05stateB\xdd\x01\n\x17\x63om.vdp.pipeline.v1betaB\x0e\x43onnectorProtoP\x01ZDgithub.com/instill-ai/protogen-go/vdp/pipeline/v1beta;pipelinev1beta\xa2\x02\x03VPX\xaa\x02\x13Vdp.Pipeline.V1beta\xca\x02\x13Vdp\\Pipeline\\V1beta\xe2\x02\x1fVdp\\Pipeline\\V1beta\\GPBMetadata\xea\x02\x15Vdp::Pipeline::V1betab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'vdp.pipeline.v1beta.connector_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027com.vdp.pipeline.v1betaB\016ConnectorProtoP\001ZDgithub.com/instill-ai/protogen-go/vdp/pipeline/v1beta;pipelinev1beta\242\002\003VPX\252\002\023Vdp.Pipeline.V1beta\312\002\023Vdp\\Pipeline\\V1beta\342\002\037Vdp\\Pipeline\\V1beta\\GPBMetadata\352\002\025Vdp::Pipeline::V1beta'
  _CONNECTOR.fields_by_name['name']._options = None
  _CONNECTOR.fields_by_name['name']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['uid']._options = None
  _CONNECTOR.fields_by_name['uid']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['id']._options = None
  _CONNECTOR.fields_by_name['id']._serialized_options = b'\342A\001\005'
  _CONNECTOR.fields_by_name['connector_definition_name']._options = None
  _CONNECTOR.fields_by_name['connector_definition_name']._serialized_options = b'\342A\001\005\372A&\n$api.instill.tech/ConnectorDefinition'
  _CONNECTOR.fields_by_name['type']._options = None
  _CONNECTOR.fields_by_name['type']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['description']._options = None
  _CONNECTOR.fields_by_name['description']._serialized_options = b'\342A\001\001'
  _CONNECTOR.fields_by_name['configuration']._options = None
  _CONNECTOR.fields_by_name['configuration']._serialized_options = b'\342A\001\002'
  _CONNECTOR.fields_by_name['state']._options = None
  _CONNECTOR.fields_by_name['state']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['tombstone']._options = None
  _CONNECTOR.fields_by_name['tombstone']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['create_time']._options = None
  _CONNECTOR.fields_by_name['create_time']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['update_time']._options = None
  _CONNECTOR.fields_by_name['update_time']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['visibility']._options = None
  _CONNECTOR.fields_by_name['visibility']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['connector_definition']._options = None
  _CONNECTOR.fields_by_name['connector_definition']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['delete_time']._options = None
  _CONNECTOR.fields_by_name['delete_time']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['owner_name']._options = None
  _CONNECTOR.fields_by_name['owner_name']._serialized_options = b'\342A\001\003'
  _CONNECTOR.fields_by_name['owner']._options = None
  _CONNECTOR.fields_by_name['owner']._serialized_options = b'\342A\001\003'
  _CONNECTOR._options = None
  _CONNECTOR._serialized_options = b'\352A?\n\032api.instill.tech/Connector\022\017connectors/{id}\022\020connectors/{uid}'
  _LISTCONNECTORSREQUEST.fields_by_name['page_size']._options = None
  _LISTCONNECTORSREQUEST.fields_by_name['page_size']._serialized_options = b'\342A\001\001'
  _LISTCONNECTORSREQUEST.fields_by_name['page_token']._options = None
  _LISTCONNECTORSREQUEST.fields_by_name['page_token']._serialized_options = b'\342A\001\001'
  _LISTCONNECTORSREQUEST.fields_by_name['view']._options = None
  _LISTCONNECTORSREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _LISTCONNECTORSREQUEST.fields_by_name['filter']._options = None
  _LISTCONNECTORSREQUEST.fields_by_name['filter']._serialized_options = b'\342A\001\001'
  _LISTCONNECTORSREQUEST.fields_by_name['show_deleted']._options = None
  _LISTCONNECTORSREQUEST.fields_by_name['show_deleted']._serialized_options = b'\342A\001\001'
  _LOOKUPCONNECTORREQUEST.fields_by_name['permalink']._options = None
  _LOOKUPCONNECTORREQUEST.fields_by_name['permalink']._serialized_options = b'\222A#\312> \372\002\035operator_definition.permalink\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _LOOKUPCONNECTORREQUEST.fields_by_name['view']._options = None
  _LOOKUPCONNECTORREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _CREATEUSERCONNECTORREQUEST.fields_by_name['connector']._options = None
  _CREATEUSERCONNECTORREQUEST.fields_by_name['connector']._serialized_options = b'\342A\001\002'
  _CREATEUSERCONNECTORREQUEST.fields_by_name['parent']._options = None
  _CREATEUSERCONNECTORREQUEST.fields_by_name['parent']._serialized_options = b'\342A\001\002\372A\034\022\032api.instill.tech/Connector'
  _LISTUSERCONNECTORSREQUEST.fields_by_name['page_size']._options = None
  _LISTUSERCONNECTORSREQUEST.fields_by_name['page_size']._serialized_options = b'\342A\001\001'
  _LISTUSERCONNECTORSREQUEST.fields_by_name['page_token']._options = None
  _LISTUSERCONNECTORSREQUEST.fields_by_name['page_token']._serialized_options = b'\342A\001\001'
  _LISTUSERCONNECTORSREQUEST.fields_by_name['view']._options = None
  _LISTUSERCONNECTORSREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _LISTUSERCONNECTORSREQUEST.fields_by_name['filter']._options = None
  _LISTUSERCONNECTORSREQUEST.fields_by_name['filter']._serialized_options = b'\342A\001\001'
  _LISTUSERCONNECTORSREQUEST.fields_by_name['parent']._options = None
  _LISTUSERCONNECTORSREQUEST.fields_by_name['parent']._serialized_options = b'\342A\001\002\372A\034\022\032api.instill.tech/Connector'
  _LISTUSERCONNECTORSREQUEST.fields_by_name['show_deleted']._options = None
  _LISTUSERCONNECTORSREQUEST.fields_by_name['show_deleted']._serialized_options = b'\342A\001\001'
  _GETUSERCONNECTORREQUEST.fields_by_name['name']._options = None
  _GETUSERCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\222A\024\312>\021\372\002\016connector.name\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _GETUSERCONNECTORREQUEST.fields_by_name['view']._options = None
  _GETUSERCONNECTORREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _UPDATEUSERCONNECTORREQUEST.fields_by_name['connector']._options = None
  _UPDATEUSERCONNECTORREQUEST.fields_by_name['connector']._serialized_options = b'\342A\001\002'
  _UPDATEUSERCONNECTORREQUEST.fields_by_name['update_mask']._options = None
  _UPDATEUSERCONNECTORREQUEST.fields_by_name['update_mask']._serialized_options = b'\342A\001\002'
  _DELETEUSERCONNECTORREQUEST.fields_by_name['name']._options = None
  _DELETEUSERCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\222A\024\312>\021\372\002\016connector.name\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _CONNECTUSERCONNECTORREQUEST.fields_by_name['name']._options = None
  _CONNECTUSERCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _DISCONNECTUSERCONNECTORREQUEST.fields_by_name['name']._options = None
  _DISCONNECTUSERCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _RENAMEUSERCONNECTORREQUEST.fields_by_name['name']._options = None
  _RENAMEUSERCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _RENAMEUSERCONNECTORREQUEST.fields_by_name['new_connector_id']._options = None
  _RENAMEUSERCONNECTORREQUEST.fields_by_name['new_connector_id']._serialized_options = b'\342A\001\002'
  _EXECUTEUSERCONNECTORREQUEST.fields_by_name['name']._options = None
  _EXECUTEUSERCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\342A\001\002'
  _TESTUSERCONNECTORREQUEST.fields_by_name['name']._options = None
  _TESTUSERCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\222A\024\312>\021\372\002\016connector.name\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _WATCHUSERCONNECTORREQUEST.fields_by_name['name']._options = None
  _WATCHUSERCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\222A\024\312>\021\372\002\016connector.name\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _CREATEORGANIZATIONCONNECTORREQUEST.fields_by_name['connector']._options = None
  _CREATEORGANIZATIONCONNECTORREQUEST.fields_by_name['connector']._serialized_options = b'\342A\001\002'
  _CREATEORGANIZATIONCONNECTORREQUEST.fields_by_name['parent']._options = None
  _CREATEORGANIZATIONCONNECTORREQUEST.fields_by_name['parent']._serialized_options = b'\342A\001\002\372A\034\022\032api.instill.tech/Connector'
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['page_size']._options = None
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['page_size']._serialized_options = b'\342A\001\001'
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['page_token']._options = None
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['page_token']._serialized_options = b'\342A\001\001'
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['view']._options = None
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['filter']._options = None
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['filter']._serialized_options = b'\342A\001\001'
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['parent']._options = None
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['parent']._serialized_options = b'\342A\001\002\372A\034\022\032api.instill.tech/Connector'
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['show_deleted']._options = None
  _LISTORGANIZATIONCONNECTORSREQUEST.fields_by_name['show_deleted']._serialized_options = b'\342A\001\001'
  _GETORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._options = None
  _GETORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\222A\024\312>\021\372\002\016connector.name\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _GETORGANIZATIONCONNECTORREQUEST.fields_by_name['view']._options = None
  _GETORGANIZATIONCONNECTORREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _UPDATEORGANIZATIONCONNECTORREQUEST.fields_by_name['connector']._options = None
  _UPDATEORGANIZATIONCONNECTORREQUEST.fields_by_name['connector']._serialized_options = b'\342A\001\002'
  _UPDATEORGANIZATIONCONNECTORREQUEST.fields_by_name['update_mask']._options = None
  _UPDATEORGANIZATIONCONNECTORREQUEST.fields_by_name['update_mask']._serialized_options = b'\342A\001\002'
  _DELETEORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._options = None
  _DELETEORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\222A\024\312>\021\372\002\016connector.name\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _CONNECTORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._options = None
  _CONNECTORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _DISCONNECTORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._options = None
  _DISCONNECTORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _RENAMEORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._options = None
  _RENAMEORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _RENAMEORGANIZATIONCONNECTORREQUEST.fields_by_name['new_connector_id']._options = None
  _RENAMEORGANIZATIONCONNECTORREQUEST.fields_by_name['new_connector_id']._serialized_options = b'\342A\001\002'
  _EXECUTEORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._options = None
  _EXECUTEORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\342A\001\002'
  _TESTORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._options = None
  _TESTORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\222A\024\312>\021\372\002\016connector.name\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _WATCHORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._options = None
  _WATCHORGANIZATIONCONNECTORREQUEST.fields_by_name['name']._serialized_options = b'\222A\024\312>\021\372\002\016connector.name\342A\001\002\372A\034\n\032api.instill.tech/Connector'
  _LISTCONNECTORSADMINREQUEST.fields_by_name['page_size']._options = None
  _LISTCONNECTORSADMINREQUEST.fields_by_name['page_size']._serialized_options = b'\342A\001\001'
  _LISTCONNECTORSADMINREQUEST.fields_by_name['page_token']._options = None
  _LISTCONNECTORSADMINREQUEST.fields_by_name['page_token']._serialized_options = b'\342A\001\001'
  _LISTCONNECTORSADMINREQUEST.fields_by_name['view']._options = None
  _LISTCONNECTORSADMINREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _LISTCONNECTORSADMINREQUEST.fields_by_name['filter']._options = None
  _LISTCONNECTORSADMINREQUEST.fields_by_name['filter']._serialized_options = b'\342A\001\001'
  _LISTCONNECTORSADMINREQUEST.fields_by_name['show_deleted']._options = None
  _LISTCONNECTORSADMINREQUEST.fields_by_name['show_deleted']._serialized_options = b'\342A\001\001'
  _LOOKUPCONNECTORADMINREQUEST.fields_by_name['permalink']._options = None
  _LOOKUPCONNECTORADMINREQUEST.fields_by_name['permalink']._serialized_options = b'\342A\001\002'
  _LOOKUPCONNECTORADMINREQUEST.fields_by_name['view']._options = None
  _LOOKUPCONNECTORADMINREQUEST.fields_by_name['view']._serialized_options = b'\342A\001\001'
  _CHECKCONNECTORREQUEST.fields_by_name['permalink']._options = None
  _CHECKCONNECTORREQUEST.fields_by_name['permalink']._serialized_options = b'\342A\001\002'
  _globals['_CONNECTOR']._serialized_start=314
  _globals['_CONNECTOR']._serialized_end=1605
  _globals['_CONNECTOR_VIEW']._serialized_start=1255
  _globals['_CONNECTOR_VIEW']._serialized_end=1338
  _globals['_CONNECTOR_STATE']._serialized_start=1340
  _globals['_CONNECTOR_STATE']._serialized_end=1432
  _globals['_CONNECTOR_VISIBILITY']._serialized_start=1434
  _globals['_CONNECTOR_VISIBILITY']._serialized_end=1521
  _globals['_LISTCONNECTORSREQUEST']._serialized_start=1608
  _globals['_LISTCONNECTORSREQUEST']._serialized_end=1928
  _globals['_LISTCONNECTORSRESPONSE']._serialized_start=1931
  _globals['_LISTCONNECTORSRESPONSE']._serialized_end=2090
  _globals['_LOOKUPCONNECTORREQUEST']._serialized_start=2093
  _globals['_LOOKUPCONNECTORREQUEST']._serialized_end=2299
  _globals['_LOOKUPCONNECTORRESPONSE']._serialized_start=2301
  _globals['_LOOKUPCONNECTORRESPONSE']._serialized_end=2388
  _globals['_CREATEUSERCONNECTORREQUEST']._serialized_start=2391
  _globals['_CREATEUSERCONNECTORREQUEST']._serialized_end=2548
  _globals['_CREATEUSERCONNECTORRESPONSE']._serialized_start=2550
  _globals['_CREATEUSERCONNECTORRESPONSE']._serialized_end=2641
  _globals['_LISTUSERCONNECTORSREQUEST']._serialized_start=2644
  _globals['_LISTUSERCONNECTORSREQUEST']._serialized_end=3029
  _globals['_LISTUSERCONNECTORSRESPONSE']._serialized_start=3032
  _globals['_LISTUSERCONNECTORSRESPONSE']._serialized_end=3195
  _globals['_GETUSERCONNECTORREQUEST']._serialized_start=3198
  _globals['_GETUSERCONNECTORREQUEST']._serialized_end=3380
  _globals['_GETUSERCONNECTORRESPONSE']._serialized_start=3382
  _globals['_GETUSERCONNECTORRESPONSE']._serialized_end=3470
  _globals['_UPDATEUSERCONNECTORREQUEST']._serialized_start=3473
  _globals['_UPDATEUSERCONNECTORREQUEST']._serialized_end=3636
  _globals['_UPDATEUSERCONNECTORRESPONSE']._serialized_start=3638
  _globals['_UPDATEUSERCONNECTORRESPONSE']._serialized_end=3729
  _globals['_DELETEUSERCONNECTORREQUEST']._serialized_start=3731
  _globals['_DELETEUSERCONNECTORREQUEST']._serialized_end=3839
  _globals['_DELETEUSERCONNECTORRESPONSE']._serialized_start=3841
  _globals['_DELETEUSERCONNECTORRESPONSE']._serialized_end=3870
  _globals['_CONNECTUSERCONNECTORREQUEST']._serialized_start=3872
  _globals['_CONNECTUSERCONNECTORREQUEST']._serialized_end=3958
  _globals['_CONNECTUSERCONNECTORRESPONSE']._serialized_start=3960
  _globals['_CONNECTUSERCONNECTORRESPONSE']._serialized_end=4052
  _globals['_DISCONNECTUSERCONNECTORREQUEST']._serialized_start=4054
  _globals['_DISCONNECTUSERCONNECTORREQUEST']._serialized_end=4143
  _globals['_DISCONNECTUSERCONNECTORRESPONSE']._serialized_start=4145
  _globals['_DISCONNECTUSERCONNECTORRESPONSE']._serialized_end=4240
  _globals['_RENAMEUSERCONNECTORREQUEST']._serialized_start=4243
  _globals['_RENAMEUSERCONNECTORREQUEST']._serialized_end=4376
  _globals['_RENAMEUSERCONNECTORRESPONSE']._serialized_start=4378
  _globals['_RENAMEUSERCONNECTORRESPONSE']._serialized_end=4469
  _globals['_EXECUTEUSERCONNECTORREQUEST']._serialized_start=4471
  _globals['_EXECUTEUSERCONNECTORREQUEST']._serialized_end=4595
  _globals['_EXECUTEUSERCONNECTORRESPONSE']._serialized_start=4597
  _globals['_EXECUTEUSERCONNECTORRESPONSE']._serialized_end=4678
  _globals['_TESTUSERCONNECTORREQUEST']._serialized_start=4680
  _globals['_TESTUSERCONNECTORREQUEST']._serialized_end=4786
  _globals['_TESTUSERCONNECTORRESPONSE']._serialized_start=4788
  _globals['_TESTUSERCONNECTORRESPONSE']._serialized_end=4875
  _globals['_WATCHUSERCONNECTORREQUEST']._serialized_start=4877
  _globals['_WATCHUSERCONNECTORREQUEST']._serialized_end=4984
  _globals['_WATCHUSERCONNECTORRESPONSE']._serialized_start=4986
  _globals['_WATCHUSERCONNECTORRESPONSE']._serialized_end=5074
  _globals['_CREATEORGANIZATIONCONNECTORREQUEST']._serialized_start=5077
  _globals['_CREATEORGANIZATIONCONNECTORREQUEST']._serialized_end=5242
  _globals['_CREATEORGANIZATIONCONNECTORRESPONSE']._serialized_start=5244
  _globals['_CREATEORGANIZATIONCONNECTORRESPONSE']._serialized_end=5343
  _globals['_LISTORGANIZATIONCONNECTORSREQUEST']._serialized_start=5346
  _globals['_LISTORGANIZATIONCONNECTORSREQUEST']._serialized_end=5739
  _globals['_LISTORGANIZATIONCONNECTORSRESPONSE']._serialized_start=5742
  _globals['_LISTORGANIZATIONCONNECTORSRESPONSE']._serialized_end=5913
  _globals['_GETORGANIZATIONCONNECTORREQUEST']._serialized_start=5916
  _globals['_GETORGANIZATIONCONNECTORREQUEST']._serialized_end=6106
  _globals['_GETORGANIZATIONCONNECTORRESPONSE']._serialized_start=6108
  _globals['_GETORGANIZATIONCONNECTORRESPONSE']._serialized_end=6204
  _globals['_UPDATEORGANIZATIONCONNECTORREQUEST']._serialized_start=6207
  _globals['_UPDATEORGANIZATIONCONNECTORREQUEST']._serialized_end=6378
  _globals['_UPDATEORGANIZATIONCONNECTORRESPONSE']._serialized_start=6380
  _globals['_UPDATEORGANIZATIONCONNECTORRESPONSE']._serialized_end=6479
  _globals['_DELETEORGANIZATIONCONNECTORREQUEST']._serialized_start=6481
  _globals['_DELETEORGANIZATIONCONNECTORREQUEST']._serialized_end=6597
  _globals['_DELETEORGANIZATIONCONNECTORRESPONSE']._serialized_start=6599
  _globals['_DELETEORGANIZATIONCONNECTORRESPONSE']._serialized_end=6636
  _globals['_CONNECTORGANIZATIONCONNECTORREQUEST']._serialized_start=6638
  _globals['_CONNECTORGANIZATIONCONNECTORREQUEST']._serialized_end=6732
  _globals['_CONNECTORGANIZATIONCONNECTORRESPONSE']._serialized_start=6734
  _globals['_CONNECTORGANIZATIONCONNECTORRESPONSE']._serialized_end=6834
  _globals['_DISCONNECTORGANIZATIONCONNECTORREQUEST']._serialized_start=6836
  _globals['_DISCONNECTORGANIZATIONCONNECTORREQUEST']._serialized_end=6933
  _globals['_DISCONNECTORGANIZATIONCONNECTORRESPONSE']._serialized_start=6935
  _globals['_DISCONNECTORGANIZATIONCONNECTORRESPONSE']._serialized_end=7038
  _globals['_RENAMEORGANIZATIONCONNECTORREQUEST']._serialized_start=7041
  _globals['_RENAMEORGANIZATIONCONNECTORREQUEST']._serialized_end=7182
  _globals['_RENAMEORGANIZATIONCONNECTORRESPONSE']._serialized_start=7184
  _globals['_RENAMEORGANIZATIONCONNECTORRESPONSE']._serialized_end=7283
  _globals['_EXECUTEORGANIZATIONCONNECTORREQUEST']._serialized_start=7286
  _globals['_EXECUTEORGANIZATIONCONNECTORREQUEST']._serialized_end=7418
  _globals['_EXECUTEORGANIZATIONCONNECTORRESPONSE']._serialized_start=7420
  _globals['_EXECUTEORGANIZATIONCONNECTORRESPONSE']._serialized_end=7509
  _globals['_TESTORGANIZATIONCONNECTORREQUEST']._serialized_start=7511
  _globals['_TESTORGANIZATIONCONNECTORREQUEST']._serialized_end=7625
  _globals['_TESTORGANIZATIONCONNECTORRESPONSE']._serialized_start=7627
  _globals['_TESTORGANIZATIONCONNECTORRESPONSE']._serialized_end=7722
  _globals['_WATCHORGANIZATIONCONNECTORREQUEST']._serialized_start=7724
  _globals['_WATCHORGANIZATIONCONNECTORREQUEST']._serialized_end=7839
  _globals['_WATCHORGANIZATIONCONNECTORRESPONSE']._serialized_start=7841
  _globals['_WATCHORGANIZATIONCONNECTORRESPONSE']._serialized_end=7937
  _globals['_LISTCONNECTORSADMINREQUEST']._serialized_start=7940
  _globals['_LISTCONNECTORSADMINREQUEST']._serialized_end=8265
  _globals['_LISTCONNECTORSADMINRESPONSE']._serialized_start=8268
  _globals['_LISTCONNECTORSADMINRESPONSE']._serialized_end=8432
  _globals['_LOOKUPCONNECTORADMINREQUEST']._serialized_start=8435
  _globals['_LOOKUPCONNECTORADMINREQUEST']._serialized_end=8577
  _globals['_LOOKUPCONNECTORADMINRESPONSE']._serialized_start=8579
  _globals['_LOOKUPCONNECTORADMINRESPONSE']._serialized_end=8671
  _globals['_CHECKCONNECTORREQUEST']._serialized_start=8673
  _globals['_CHECKCONNECTORREQUEST']._serialized_end=8732
  _globals['_CHECKCONNECTORRESPONSE']._serialized_start=8734
  _globals['_CHECKCONNECTORRESPONSE']._serialized_end=8818
# @@protoc_insertion_point(module_scope)
