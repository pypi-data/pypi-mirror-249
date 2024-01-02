# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: model/model/v1alpha/task_text_generation_chat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from model.model.v1alpha import common_pb2 as model_dot_model_dot_v1alpha_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3model/model/v1alpha/task_text_generation_chat.proto\x12\x13model.model.v1alpha\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a model/model/v1alpha/common.proto\"\xa5\x04\n\x17TextGenerationChatInput\x12\x1c\n\x06prompt\x18\x01 \x01(\tB\x04\xe2\x41\x01\x02R\x06prompt\x12K\n\rprompt_images\x18\x02 \x03(\x0b\x32 .model.model.v1alpha.PromptImageB\x04\xe2\x41\x01\x01R\x0cpromptImages\x12\x45\n\x0c\x63hat_history\x18\x03 \x03(\x0b\x32\x1c.model.model.v1alpha.ContentB\x04\xe2\x41\x01\x01R\x0b\x63hatHistory\x12\x30\n\x0esystem_message\x18\x04 \x01(\tB\x04\xe2\x41\x01\x01H\x00R\rsystemMessage\x88\x01\x01\x12/\n\x0emax_new_tokens\x18\x05 \x01(\x05\x42\x04\xe2\x41\x01\x01H\x01R\x0cmaxNewTokens\x88\x01\x01\x12+\n\x0btemperature\x18\x06 \x01(\x02\x42\x04\xe2\x41\x01\x01H\x02R\x0btemperature\x88\x01\x01\x12\x1e\n\x05top_k\x18\x07 \x01(\x05\x42\x04\xe2\x41\x01\x01H\x03R\x04topK\x88\x01\x01\x12\x1d\n\x04seed\x18\x08 \x01(\x05\x42\x04\xe2\x41\x01\x01H\x04R\x04seed\x88\x01\x01\x12@\n\x0c\x65xtra_params\x18\t \x01(\x0b\x32\x17.google.protobuf.StructB\x04\xe2\x41\x01\x01R\x0b\x65xtraParamsB\x11\n\x0f_system_messageB\x11\n\x0f_max_new_tokensB\x0e\n\x0c_temperatureB\x08\n\x06_top_kB\x07\n\x05_seed\"4\n\x18TextGenerationChatOutput\x12\x18\n\x04text\x18\x01 \x01(\tB\x04\xe2\x41\x01\x03R\x04textB\xe8\x01\n\x17\x63om.model.model.v1alphaB\x1bTaskTextGenerationChatProtoP\x01ZBgithub.com/instill-ai/protogen-go/model/model/v1alpha;modelv1alpha\xa2\x02\x03MMX\xaa\x02\x13Model.Model.V1alpha\xca\x02\x13Model\\Model\\V1alpha\xe2\x02\x1fModel\\Model\\V1alpha\\GPBMetadata\xea\x02\x15Model::Model::V1alphab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'model.model.v1alpha.task_text_generation_chat_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027com.model.model.v1alphaB\033TaskTextGenerationChatProtoP\001ZBgithub.com/instill-ai/protogen-go/model/model/v1alpha;modelv1alpha\242\002\003MMX\252\002\023Model.Model.V1alpha\312\002\023Model\\Model\\V1alpha\342\002\037Model\\Model\\V1alpha\\GPBMetadata\352\002\025Model::Model::V1alpha'
  _TEXTGENERATIONCHATINPUT.fields_by_name['prompt']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['prompt']._serialized_options = b'\342A\001\002'
  _TEXTGENERATIONCHATINPUT.fields_by_name['prompt_images']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['prompt_images']._serialized_options = b'\342A\001\001'
  _TEXTGENERATIONCHATINPUT.fields_by_name['chat_history']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['chat_history']._serialized_options = b'\342A\001\001'
  _TEXTGENERATIONCHATINPUT.fields_by_name['system_message']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['system_message']._serialized_options = b'\342A\001\001'
  _TEXTGENERATIONCHATINPUT.fields_by_name['max_new_tokens']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['max_new_tokens']._serialized_options = b'\342A\001\001'
  _TEXTGENERATIONCHATINPUT.fields_by_name['temperature']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['temperature']._serialized_options = b'\342A\001\001'
  _TEXTGENERATIONCHATINPUT.fields_by_name['top_k']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['top_k']._serialized_options = b'\342A\001\001'
  _TEXTGENERATIONCHATINPUT.fields_by_name['seed']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['seed']._serialized_options = b'\342A\001\001'
  _TEXTGENERATIONCHATINPUT.fields_by_name['extra_params']._options = None
  _TEXTGENERATIONCHATINPUT.fields_by_name['extra_params']._serialized_options = b'\342A\001\001'
  _TEXTGENERATIONCHATOUTPUT.fields_by_name['text']._options = None
  _TEXTGENERATIONCHATOUTPUT.fields_by_name['text']._serialized_options = b'\342A\001\003'
  _globals['_TEXTGENERATIONCHATINPUT']._serialized_start=174
  _globals['_TEXTGENERATIONCHATINPUT']._serialized_end=723
  _globals['_TEXTGENERATIONCHATOUTPUT']._serialized_start=725
  _globals['_TEXTGENERATIONCHATOUTPUT']._serialized_end=777
# @@protoc_insertion_point(module_scope)
