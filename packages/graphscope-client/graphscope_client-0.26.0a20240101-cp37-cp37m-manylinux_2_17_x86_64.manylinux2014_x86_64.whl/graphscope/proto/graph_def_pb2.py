# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: graph_def.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
import schema_common_pb2 as schema__common__pb2

from schema_common_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fgraph_def.proto\x12\x0cgs.rpc.graph\x1a\x19google/protobuf/any.proto\x1a\x13schema_common.proto\"U\n\x0bGrootInfoPb\x12\x15\n\rlast_label_id\x18\x01 \x01(\x05\x12\x18\n\x10last_property_id\x18\x02 \x01(\x05\x12\x15\n\rlast_table_id\x18\x03 \x01(\x03\"\x81\x03\n\x0eVineyardInfoPb\x12*\n\x08oid_type\x18\x01 \x01(\x0e\x32\x18.gs.rpc.graph.DataTypePb\x12*\n\x08vid_type\x18\x02 \x01(\x0e\x32\x18.gs.rpc.graph.DataTypePb\x12,\n\nvdata_type\x18\x03 \x01(\x0e\x32\x18.gs.rpc.graph.DataTypePb\x12,\n\nedata_type\x18\x04 \x01(\x0e\x32\x18.gs.rpc.graph.DataTypePb\x12\x13\n\x0bschema_path\x18\x05 \x01(\t\x12\x14\n\x0cgenerate_eid\x18\x06 \x01(\x08\x12\x13\n\x0bvineyard_id\x18\x07 \x01(\x03\x12\x1c\n\x14property_schema_json\x18\x08 \x01(\t\x12\x36\n\x0fvertex_map_type\x18\t \x01(\x0e\x32\x1d.gs.rpc.graph.VertexMapTypePb\x12\x11\n\tfragments\x18\n \x03(\x03\x12\x12\n\nretain_oid\x18\x0b \x01(\x08\"\x8e\x01\n\x12MutableGraphInfoPb\x12,\n\nvdata_type\x18\x01 \x01(\x0e\x32\x18.gs.rpc.graph.DataTypePb\x12,\n\nedata_type\x18\x02 \x01(\x0e\x32\x18.gs.rpc.graph.DataTypePb\x12\x1c\n\x14property_schema_json\x18\x03 \x01(\t\"\xbc\x03\n\nGraphDefPb\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12\x0b\n\x03key\x18\x02 \x01(\t\x12-\n\ngraph_type\x18\x03 \x01(\x0e\x32\x19.gs.rpc.graph.GraphTypePb\x12\x10\n\x08\x64irected\x18\x04 \x01(\x08\x12*\n\ttype_defs\x18\x05 \x03(\x0b\x32\x17.gs.rpc.graph.TypeDefPb\x12,\n\nedge_kinds\x18\x06 \x03(\x0b\x32\x18.gs.rpc.graph.EdgeKindPb\x12K\n\x13property_name_to_id\x18\x07 \x03(\x0b\x32..gs.rpc.graph.GraphDefPb.PropertyNameToIdEntry\x12\'\n\textension\x18\x08 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x15\n\ris_multigraph\x18\t \x01(\x08\x12\x15\n\rcompact_edges\x18\n \x01(\x08\x12\x18\n\x10use_perfect_hash\x18\x0b \x01(\x08\x1a\x37\n\x15PropertyNameToIdEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01*\xb7\x01\n\x0bGraphTypePb\x12\x10\n\x0cUNKNOWN_TYPE\x10\x00\x12\x15\n\x11IMMUTABLE_EDGECUT\x10\x01\x12\x14\n\x10\x44YNAMIC_PROPERTY\x10\x02\x12\x15\n\x11\x44YNAMIC_PROJECTED\x10\x03\x12\x12\n\x0e\x41RROW_PROPERTY\x10\x04\x12\x13\n\x0f\x41RROW_PROJECTED\x10\x05\x12\x14\n\x10PERSISTENT_STORE\x10\x06\x12\x13\n\x0f\x41RROW_FLATTENED\x10\x07*S\n\x0fVertexMapTypePb\x12\x13\n\x0fUNKNOWN_VM_TYPE\x10\x00\x12\x15\n\x11GLOBAL_VERTEX_MAP\x10\x01\x12\x14\n\x10LOCAL_VERTEX_MAP\x10\x02\x42 \n\x1c\x63om.alibaba.graphscope.protoP\x01P\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'graph_def_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.alibaba.graphscope.protoP\001'
  _globals['_GRAPHDEFPB_PROPERTYNAMETOIDENTRY']._options = None
  _globals['_GRAPHDEFPB_PROPERTYNAMETOIDENTRY']._serialized_options = b'8\001'
  _globals['_GRAPHTYPEPB']._serialized_start=1149
  _globals['_GRAPHTYPEPB']._serialized_end=1332
  _globals['_VERTEXMAPTYPEPB']._serialized_start=1334
  _globals['_VERTEXMAPTYPEPB']._serialized_end=1417
  _globals['_GROOTINFOPB']._serialized_start=81
  _globals['_GROOTINFOPB']._serialized_end=166
  _globals['_VINEYARDINFOPB']._serialized_start=169
  _globals['_VINEYARDINFOPB']._serialized_end=554
  _globals['_MUTABLEGRAPHINFOPB']._serialized_start=557
  _globals['_MUTABLEGRAPHINFOPB']._serialized_end=699
  _globals['_GRAPHDEFPB']._serialized_start=702
  _globals['_GRAPHDEFPB']._serialized_end=1146
  _globals['_GRAPHDEFPB_PROPERTYNAMETOIDENTRY']._serialized_start=1091
  _globals['_GRAPHDEFPB_PROPERTYNAMETOIDENTRY']._serialized_end=1146
# @@protoc_insertion_point(module_scope)
