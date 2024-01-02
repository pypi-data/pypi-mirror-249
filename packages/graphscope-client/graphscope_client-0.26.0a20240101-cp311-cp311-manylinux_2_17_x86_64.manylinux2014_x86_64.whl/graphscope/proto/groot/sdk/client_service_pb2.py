# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: groot/sdk/client_service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from groot.sdk import model_pb2 as groot_dot_sdk_dot_model__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1egroot/sdk/client_service.proto\x12\x0cgs.rpc.groot\x1a\x15groot/sdk/model.proto\"\x12\n\x10GetSchemaRequest\"?\n\x11GetSchemaResponse\x12*\n\x08graphDef\x18\x01 \x01(\x0b\x32\x18.gs.rpc.groot.GraphDefPb\"\x91\x01\n\x11IngestDataRequest\x12\x10\n\x08\x64\x61taPath\x18\x01 \x01(\t\x12;\n\x06\x63onfig\x18\x02 \x03(\x0b\x32+.gs.rpc.groot.IngestDataRequest.ConfigEntry\x1a-\n\x0b\x43onfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x14\n\x12IngestDataResponse\"&\n\x11GetMetricsRequest\x12\x11\n\troleNames\x18\x01 \x01(\t\")\n\x12GetMetricsResponse\x12\x13\n\x0bmetricsJson\x18\x01 \x01(\t\"+\n\x15LoadJsonSchemaRequest\x12\x12\n\nschemaJson\x18\x01 \x01(\t\"D\n\x16LoadJsonSchemaResponse\x12*\n\x08graphDef\x18\x01 \x01(\x0b\x32\x18.gs.rpc.groot.GraphDefPb\"\x13\n\x11\x44ropSchemaRequest\"@\n\x12\x44ropSchemaResponse\x12*\n\x08graphDef\x18\x01 \x01(\x0b\x32\x18.gs.rpc.groot.GraphDefPb\"Q\n\x16PrepareDataLoadRequest\x12\x37\n\x0f\x64\x61taLoadTargets\x18\x01 \x03(\x0b\x32\x1e.gs.rpc.groot.DataLoadTargetPb\"E\n\x17PrepareDataLoadResponse\x12*\n\x08graphDef\x18\x01 \x01(\x0b\x32\x18.gs.rpc.groot.GraphDefPb\"\xca\x01\n\x15\x43ommitDataLoadRequest\x12M\n\rtableToTarget\x18\x01 \x03(\x0b\x32\x36.gs.rpc.groot.CommitDataLoadRequest.TableToTargetEntry\x12\x0c\n\x04path\x18\x02 \x01(\t\x1aT\n\x12TableToTargetEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12-\n\x05value\x18\x02 \x01(\x0b\x32\x1e.gs.rpc.groot.DataLoadTargetPb:\x02\x38\x01\"\x18\n\x16\x43ommitDataLoadResponse\"\x18\n\x16GetPartitionNumRequest\"/\n\x17GetPartitionNumResponse\x12\x14\n\x0cpartitionNum\x18\x01 \x01(\x05\"\x16\n\x14GetLoggerInfoRequest\"]\n\x15GetLoggerInfoResponse\x12\x15\n\rloggerServers\x18\x01 \x01(\t\x12\x13\n\x0bloggerTopic\x18\x02 \x01(\t\x12\x18\n\x10loggerQueueCount\x18\x03 \x01(\x05\"&\n\x12\x43learIngestRequest\x12\x10\n\x08\x64\x61taPath\x18\x01 \x01(\t\"\x15\n\x13\x43learIngestResponse2\xcb\x07\n\x06\x43lient\x12L\n\tgetSchema\x12\x1e.gs.rpc.groot.GetSchemaRequest\x1a\x1f.gs.rpc.groot.GetSchemaResponse\x12O\n\ningestData\x12\x1f.gs.rpc.groot.IngestDataRequest\x1a .gs.rpc.groot.IngestDataResponse\x12O\n\ngetMetrics\x12\x1f.gs.rpc.groot.GetMetricsRequest\x1a .gs.rpc.groot.GetMetricsResponse\x12[\n\x0eloadJsonSchema\x12#.gs.rpc.groot.LoadJsonSchemaRequest\x1a$.gs.rpc.groot.LoadJsonSchemaResponse\x12O\n\ndropSchema\x12\x1f.gs.rpc.groot.DropSchemaRequest\x1a .gs.rpc.groot.DropSchemaResponse\x12^\n\x0fprepareDataLoad\x12$.gs.rpc.groot.PrepareDataLoadRequest\x1a%.gs.rpc.groot.PrepareDataLoadResponse\x12[\n\x0e\x63ommitDataLoad\x12#.gs.rpc.groot.CommitDataLoadRequest\x1a$.gs.rpc.groot.CommitDataLoadResponse\x12^\n\x0fgetPartitionNum\x12$.gs.rpc.groot.GetPartitionNumRequest\x1a%.gs.rpc.groot.GetPartitionNumResponse\x12X\n\rgetLoggerInfo\x12\".gs.rpc.groot.GetLoggerInfoRequest\x1a#.gs.rpc.groot.GetLoggerInfoResponse\x12R\n\x0b\x63learIngest\x12 .gs.rpc.groot.ClearIngestRequest\x1a!.gs.rpc.groot.ClearIngestResponse\x12X\n\rgetStoreState\x12\".gs.rpc.groot.GetStoreStateRequest\x1a#.gs.rpc.groot.GetStoreStateResponseB&\n\"com.alibaba.graphscope.proto.grootP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'groot.sdk.client_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"com.alibaba.graphscope.proto.grootP\001'
  _globals['_INGESTDATAREQUEST_CONFIGENTRY']._options = None
  _globals['_INGESTDATAREQUEST_CONFIGENTRY']._serialized_options = b'8\001'
  _globals['_COMMITDATALOADREQUEST_TABLETOTARGETENTRY']._options = None
  _globals['_COMMITDATALOADREQUEST_TABLETOTARGETENTRY']._serialized_options = b'8\001'
  _globals['_GETSCHEMAREQUEST']._serialized_start=71
  _globals['_GETSCHEMAREQUEST']._serialized_end=89
  _globals['_GETSCHEMARESPONSE']._serialized_start=91
  _globals['_GETSCHEMARESPONSE']._serialized_end=154
  _globals['_INGESTDATAREQUEST']._serialized_start=157
  _globals['_INGESTDATAREQUEST']._serialized_end=302
  _globals['_INGESTDATAREQUEST_CONFIGENTRY']._serialized_start=257
  _globals['_INGESTDATAREQUEST_CONFIGENTRY']._serialized_end=302
  _globals['_INGESTDATARESPONSE']._serialized_start=304
  _globals['_INGESTDATARESPONSE']._serialized_end=324
  _globals['_GETMETRICSREQUEST']._serialized_start=326
  _globals['_GETMETRICSREQUEST']._serialized_end=364
  _globals['_GETMETRICSRESPONSE']._serialized_start=366
  _globals['_GETMETRICSRESPONSE']._serialized_end=407
  _globals['_LOADJSONSCHEMAREQUEST']._serialized_start=409
  _globals['_LOADJSONSCHEMAREQUEST']._serialized_end=452
  _globals['_LOADJSONSCHEMARESPONSE']._serialized_start=454
  _globals['_LOADJSONSCHEMARESPONSE']._serialized_end=522
  _globals['_DROPSCHEMAREQUEST']._serialized_start=524
  _globals['_DROPSCHEMAREQUEST']._serialized_end=543
  _globals['_DROPSCHEMARESPONSE']._serialized_start=545
  _globals['_DROPSCHEMARESPONSE']._serialized_end=609
  _globals['_PREPAREDATALOADREQUEST']._serialized_start=611
  _globals['_PREPAREDATALOADREQUEST']._serialized_end=692
  _globals['_PREPAREDATALOADRESPONSE']._serialized_start=694
  _globals['_PREPAREDATALOADRESPONSE']._serialized_end=763
  _globals['_COMMITDATALOADREQUEST']._serialized_start=766
  _globals['_COMMITDATALOADREQUEST']._serialized_end=968
  _globals['_COMMITDATALOADREQUEST_TABLETOTARGETENTRY']._serialized_start=884
  _globals['_COMMITDATALOADREQUEST_TABLETOTARGETENTRY']._serialized_end=968
  _globals['_COMMITDATALOADRESPONSE']._serialized_start=970
  _globals['_COMMITDATALOADRESPONSE']._serialized_end=994
  _globals['_GETPARTITIONNUMREQUEST']._serialized_start=996
  _globals['_GETPARTITIONNUMREQUEST']._serialized_end=1020
  _globals['_GETPARTITIONNUMRESPONSE']._serialized_start=1022
  _globals['_GETPARTITIONNUMRESPONSE']._serialized_end=1069
  _globals['_GETLOGGERINFOREQUEST']._serialized_start=1071
  _globals['_GETLOGGERINFOREQUEST']._serialized_end=1093
  _globals['_GETLOGGERINFORESPONSE']._serialized_start=1095
  _globals['_GETLOGGERINFORESPONSE']._serialized_end=1188
  _globals['_CLEARINGESTREQUEST']._serialized_start=1190
  _globals['_CLEARINGESTREQUEST']._serialized_end=1228
  _globals['_CLEARINGESTRESPONSE']._serialized_start=1230
  _globals['_CLEARINGESTRESPONSE']._serialized_end=1251
  _globals['_CLIENT']._serialized_start=1254
  _globals['_CLIENT']._serialized_end=2225
# @@protoc_insertion_point(module_scope)
