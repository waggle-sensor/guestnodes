# Generated by the protocol buffer compiler.  DO NOT EDIT!
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
# source: object_detection/protos/faster_rcnn_box_coder.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='object_detection/protos/faster_rcnn_box_coder.proto',
  package='object_detection.protos',
  syntax='proto2',
  serialized_pb=_b('\n3object_detection/protos/faster_rcnn_box_coder.proto\x12\x17object_detection.protos\"o\n\x12\x46\x61sterRcnnBoxCoder\x12\x13\n\x07y_scale\x18\x01 \x01(\x02:\x02\x31\x30\x12\x13\n\x07x_scale\x18\x02 \x01(\x02:\x02\x31\x30\x12\x17\n\x0cheight_scale\x18\x03 \x01(\x02:\x01\x35\x12\x16\n\x0bwidth_scale\x18\x04 \x01(\x02:\x01\x35')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_FASTERRCNNBOXCODER = _descriptor.Descriptor(
  name='FasterRcnnBoxCoder',
  full_name='object_detection.protos.FasterRcnnBoxCoder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='y_scale', full_name='object_detection.protos.FasterRcnnBoxCoder.y_scale', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(10),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x_scale', full_name='object_detection.protos.FasterRcnnBoxCoder.x_scale', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(10),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height_scale', full_name='object_detection.protos.FasterRcnnBoxCoder.height_scale', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='width_scale', full_name='object_detection.protos.FasterRcnnBoxCoder.width_scale', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=191,
)

DESCRIPTOR.message_types_by_name['FasterRcnnBoxCoder'] = _FASTERRCNNBOXCODER

FasterRcnnBoxCoder = _reflection.GeneratedProtocolMessageType('FasterRcnnBoxCoder', (_message.Message,), dict(
  DESCRIPTOR = _FASTERRCNNBOXCODER,
  __module__ = 'object_detection.protos.faster_rcnn_box_coder_pb2'
  # @@protoc_insertion_point(class_scope:object_detection.protos.FasterRcnnBoxCoder)
  ))
_sym_db.RegisterMessage(FasterRcnnBoxCoder)


# @@protoc_insertion_point(module_scope)
