# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/administration/authenticated_user/v1/details.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7qwak/administration/authenticated_user/v1/details.proto\x12)qwak.administration.authenticated_user.v1\"/\n\x0bUserDetails\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\"|\n\x12\x45nvironmentDetails\x12\n\n\x02id\x18\x01 \x01(\t\x12Z\n\rconfiguration\x18\x02 \x01(\x0b\x32\x43.qwak.administration.authenticated_user.v1.EnvironmentConfiguration\"\xa5\x02\n\x18\x45nvironmentConfiguration\x12\x19\n\x11\x65\x64ge_services_url\x18\x01 \x01(\t\x12\x1d\n\x15management_access_url\x18\x06 \x01(\t\x12\x15\n\rmodel_api_url\x18\x02 \x01(\t\x12\x1e\n\x16\x61nalytics_data_api_url\x18\x03 \x01(\t\x12\x1d\n\x15object_storage_bucket\x18\x04 \x01(\t\x12\x19\n\x11\x62i_system_api_key\x18\x05 \x01(\t\x12^\n\x13\x63loud_configuration\x18\x07 \x01(\x0b\x32\x41.qwak.administration.authenticated_user.v1.QwakCloudConfiguration\"\x8e\x01\n\x16QwakCloudConfiguration\x12\x63\n\x17\x61ws_cloud_configuration\x18\x01 \x01(\x0b\x32@.qwak.administration.authenticated_user.v1.AwsCloudConfigurationH\x00\x42\x0f\n\rconfiguration\"a\n\x15\x41wsCloudConfiguration\x12\x0e\n\x06region\x18\x01 \x01(\t\x12\x10\n\x08role_arn\x18\x02 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x03 \x01(\t\x12\x11\n\tworkgroup\x18\x04 \x01(\tBN\n4com.qwak.ai.administration.api.authenticated_user.v1P\x01Z\x14.;authenticated_userb\x06proto3')



_USERDETAILS = DESCRIPTOR.message_types_by_name['UserDetails']
_ENVIRONMENTDETAILS = DESCRIPTOR.message_types_by_name['EnvironmentDetails']
_ENVIRONMENTCONFIGURATION = DESCRIPTOR.message_types_by_name['EnvironmentConfiguration']
_QWAKCLOUDCONFIGURATION = DESCRIPTOR.message_types_by_name['QwakCloudConfiguration']
_AWSCLOUDCONFIGURATION = DESCRIPTOR.message_types_by_name['AwsCloudConfiguration']
UserDetails = _reflection.GeneratedProtocolMessageType('UserDetails', (_message.Message,), {
  'DESCRIPTOR' : _USERDETAILS,
  '__module__' : 'qwak.administration.authenticated_user.v1.details_pb2'
  # @@protoc_insertion_point(class_scope:qwak.administration.authenticated_user.v1.UserDetails)
  })
_sym_db.RegisterMessage(UserDetails)

EnvironmentDetails = _reflection.GeneratedProtocolMessageType('EnvironmentDetails', (_message.Message,), {
  'DESCRIPTOR' : _ENVIRONMENTDETAILS,
  '__module__' : 'qwak.administration.authenticated_user.v1.details_pb2'
  # @@protoc_insertion_point(class_scope:qwak.administration.authenticated_user.v1.EnvironmentDetails)
  })
_sym_db.RegisterMessage(EnvironmentDetails)

EnvironmentConfiguration = _reflection.GeneratedProtocolMessageType('EnvironmentConfiguration', (_message.Message,), {
  'DESCRIPTOR' : _ENVIRONMENTCONFIGURATION,
  '__module__' : 'qwak.administration.authenticated_user.v1.details_pb2'
  # @@protoc_insertion_point(class_scope:qwak.administration.authenticated_user.v1.EnvironmentConfiguration)
  })
_sym_db.RegisterMessage(EnvironmentConfiguration)

QwakCloudConfiguration = _reflection.GeneratedProtocolMessageType('QwakCloudConfiguration', (_message.Message,), {
  'DESCRIPTOR' : _QWAKCLOUDCONFIGURATION,
  '__module__' : 'qwak.administration.authenticated_user.v1.details_pb2'
  # @@protoc_insertion_point(class_scope:qwak.administration.authenticated_user.v1.QwakCloudConfiguration)
  })
_sym_db.RegisterMessage(QwakCloudConfiguration)

AwsCloudConfiguration = _reflection.GeneratedProtocolMessageType('AwsCloudConfiguration', (_message.Message,), {
  'DESCRIPTOR' : _AWSCLOUDCONFIGURATION,
  '__module__' : 'qwak.administration.authenticated_user.v1.details_pb2'
  # @@protoc_insertion_point(class_scope:qwak.administration.authenticated_user.v1.AwsCloudConfiguration)
  })
_sym_db.RegisterMessage(AwsCloudConfiguration)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n4com.qwak.ai.administration.api.authenticated_user.v1P\001Z\024.;authenticated_user'
  _USERDETAILS._serialized_start=102
  _USERDETAILS._serialized_end=149
  _ENVIRONMENTDETAILS._serialized_start=151
  _ENVIRONMENTDETAILS._serialized_end=275
  _ENVIRONMENTCONFIGURATION._serialized_start=278
  _ENVIRONMENTCONFIGURATION._serialized_end=571
  _QWAKCLOUDCONFIGURATION._serialized_start=574
  _QWAKCLOUDCONFIGURATION._serialized_end=716
  _AWSCLOUDCONFIGURATION._serialized_start=718
  _AWSCLOUDCONFIGURATION._serialized_end=815
# @@protoc_insertion_point(module_scope)
