# Copyright 2015 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google BigQuery API wrapper.

The main concepts with this API are:

- :class:`~arrivy.google.cloud.bigquery.client.Client` manages connections to the
  BigQuery API. Use the client methods to run jobs (such as a
  :class:`~arrivy.google.cloud.bigquery.job.QueryJob` via
  :meth:`~arrivy.google.cloud.bigquery.client.Client.query`) and manage resources.

- :class:`~arrivy.google.cloud.bigquery.dataset.Dataset` represents a
  collection of tables.

- :class:`~arrivy.google.cloud.bigquery.table.Table` represents a single "relation".
"""


from arrivy.google.cloud.bigquery import version as bigquery_version

__version__ = bigquery_version.__version__

from arrivy.google.cloud.bigquery.client import Client
from arrivy.google.cloud.bigquery.dataset import AccessEntry
from arrivy.google.cloud.bigquery.dataset import Dataset
from arrivy.google.cloud.bigquery.dataset import DatasetReference
from arrivy.google.cloud.bigquery import enums
from arrivy.google.cloud.bigquery.enums import AutoRowIDs
from arrivy.google.cloud.bigquery.enums import DecimalTargetType
from arrivy.google.cloud.bigquery.enums import KeyResultStatementKind
from arrivy.google.cloud.bigquery.enums import SqlTypeNames
from arrivy.google.cloud.bigquery.enums import StandardSqlTypeNames
from arrivy.google.cloud.bigquery.exceptions import LegacyBigQueryStorageError
from arrivy.google.cloud.bigquery.exceptions import LegacyPyarrowError
from arrivy.google.cloud.bigquery.external_config import ExternalConfig
from arrivy.google.cloud.bigquery.external_config import BigtableOptions
from arrivy.google.cloud.bigquery.external_config import BigtableColumnFamily
from arrivy.google.cloud.bigquery.external_config import BigtableColumn
from arrivy.google.cloud.bigquery.external_config import CSVOptions
from arrivy.google.cloud.bigquery.external_config import GoogleSheetsOptions
from arrivy.google.cloud.bigquery.external_config import ExternalSourceFormat
from arrivy.google.cloud.bigquery.external_config import HivePartitioningOptions
from arrivy.google.cloud.bigquery.format_options import AvroOptions
from arrivy.google.cloud.bigquery.format_options import ParquetOptions
from arrivy.google.cloud.bigquery.job.base import SessionInfo
from arrivy.google.cloud.bigquery.job import Compression
from arrivy.google.cloud.bigquery.job import CopyJob
from arrivy.google.cloud.bigquery.job import CopyJobConfig
from arrivy.google.cloud.bigquery.job import CreateDisposition
from arrivy.google.cloud.bigquery.job import DestinationFormat
from arrivy.google.cloud.bigquery.job import DmlStats
from arrivy.google.cloud.bigquery.job import Encoding
from arrivy.google.cloud.bigquery.job import ExtractJob
from arrivy.google.cloud.bigquery.job import ExtractJobConfig
from arrivy.google.cloud.bigquery.job import LoadJob
from arrivy.google.cloud.bigquery.job import LoadJobConfig
from arrivy.google.cloud.bigquery.job import OperationType
from arrivy.google.cloud.bigquery.job import QueryJob
from arrivy.google.cloud.bigquery.job import QueryJobConfig
from arrivy.google.cloud.bigquery.job import QueryPriority
from arrivy.google.cloud.bigquery.job import SchemaUpdateOption
from arrivy.google.cloud.bigquery.job import ScriptOptions
from arrivy.google.cloud.bigquery.job import SourceFormat
from arrivy.google.cloud.bigquery.job import UnknownJob
from arrivy.google.cloud.bigquery.job import TransactionInfo
from arrivy.google.cloud.bigquery.job import WriteDisposition
from arrivy.google.cloud.bigquery.model import Model
from arrivy.google.cloud.bigquery.model import ModelReference
from arrivy.google.cloud.bigquery.query import ArrayQueryParameter
from arrivy.google.cloud.bigquery.query import ArrayQueryParameterType
from arrivy.google.cloud.bigquery.query import ConnectionProperty
from arrivy.google.cloud.bigquery.query import ScalarQueryParameter
from arrivy.google.cloud.bigquery.query import ScalarQueryParameterType
from arrivy.google.cloud.bigquery.query import SqlParameterScalarTypes
from arrivy.google.cloud.bigquery.query import StructQueryParameter
from arrivy.google.cloud.bigquery.query import StructQueryParameterType
from arrivy.google.cloud.bigquery.query import UDFResource
from arrivy.google.cloud.bigquery.retry import DEFAULT_RETRY
from arrivy.google.cloud.bigquery.routine import DeterminismLevel
from arrivy.google.cloud.bigquery.routine import Routine
from arrivy.google.cloud.bigquery.routine import RoutineArgument
from arrivy.google.cloud.bigquery.routine import RoutineReference
from arrivy.google.cloud.bigquery.routine import RoutineType
from arrivy.google.cloud.bigquery.routine import RemoteFunctionOptions
from arrivy.google.cloud.bigquery.schema import PolicyTagList
from arrivy.google.cloud.bigquery.schema import SchemaField
from arrivy.google.cloud.bigquery.standard_sql import StandardSqlDataType
from arrivy.google.cloud.bigquery.standard_sql import StandardSqlField
from arrivy.google.cloud.bigquery.standard_sql import StandardSqlStructType
from arrivy.google.cloud.bigquery.standard_sql import StandardSqlTableType
from arrivy.google.cloud.bigquery.table import PartitionRange
from arrivy.google.cloud.bigquery.table import RangePartitioning
from arrivy.google.cloud.bigquery.table import Row
from arrivy.google.cloud.bigquery.table import SnapshotDefinition
from arrivy.google.cloud.bigquery.table import CloneDefinition
from arrivy.google.cloud.bigquery.table import Table
from arrivy.google.cloud.bigquery.table import TableReference
from arrivy.google.cloud.bigquery.table import TimePartitioningType
from arrivy.google.cloud.bigquery.table import TimePartitioning
from arrivy.google.cloud.bigquery.encryption_configuration import EncryptionConfiguration

__all__ = [
    "__version__",
    "Client",
    # Queries
    "ConnectionProperty",
    "QueryJob",
    "QueryJobConfig",
    "ArrayQueryParameter",
    "ScalarQueryParameter",
    "StructQueryParameter",
    "ArrayQueryParameterType",
    "ScalarQueryParameterType",
    "SqlParameterScalarTypes",
    "StructQueryParameterType",
    # Datasets
    "Dataset",
    "DatasetReference",
    "AccessEntry",
    # Tables
    "Table",
    "TableReference",
    "PartitionRange",
    "RangePartitioning",
    "Row",
    "SnapshotDefinition",
    "CloneDefinition",
    "TimePartitioning",
    "TimePartitioningType",
    # Jobs
    "CopyJob",
    "CopyJobConfig",
    "ExtractJob",
    "ExtractJobConfig",
    "LoadJob",
    "LoadJobConfig",
    "SessionInfo",
    "UnknownJob",
    # Models
    "Model",
    "ModelReference",
    # Routines
    "Routine",
    "RoutineArgument",
    "RoutineReference",
    "RemoteFunctionOptions",
    # Shared helpers
    "SchemaField",
    "PolicyTagList",
    "UDFResource",
    "ExternalConfig",
    "AvroOptions",
    "BigtableOptions",
    "BigtableColumnFamily",
    "BigtableColumn",
    "DmlStats",
    "CSVOptions",
    "GoogleSheetsOptions",
    "HivePartitioningOptions",
    "ParquetOptions",
    "ScriptOptions",
    "TransactionInfo",
    "DEFAULT_RETRY",
    # Standard SQL types
    "StandardSqlDataType",
    "StandardSqlField",
    "StandardSqlStructType",
    "StandardSqlTableType",
    # Enum Constants
    "enums",
    "AutoRowIDs",
    "Compression",
    "CreateDisposition",
    "DecimalTargetType",
    "DestinationFormat",
    "DeterminismLevel",
    "ExternalSourceFormat",
    "Encoding",
    "KeyResultStatementKind",
    "OperationType",
    "QueryPriority",
    "RoutineType",
    "SchemaUpdateOption",
    "SourceFormat",
    "SqlTypeNames",
    "StandardSqlTypeNames",
    "WriteDisposition",
    # EncryptionConfiguration
    "EncryptionConfiguration",
    # Custom exceptions
    "LegacyBigQueryStorageError",
    "LegacyPyarrowError",
    "LegacyPandasError",
]


def load_ipython_extension(ipython):
    """Called by IPython when this module is loaded as an IPython extension."""
    from arrivy.google.cloud.bigquery.magics.magics import _cell_magic

    ipython.register_magic_function(
        _cell_magic, magic_kind="cell", magic_name="bigquery"
    )
