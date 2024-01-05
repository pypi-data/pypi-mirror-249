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

"""Define API Jobs."""

from arrivy.google.cloud.bigquery.job.base import _AsyncJob
from arrivy.google.cloud.bigquery.job.base import _error_result_to_exception
from arrivy.google.cloud.bigquery.job.base import _DONE_STATE
from arrivy.google.cloud.bigquery.job.base import _JobConfig
from arrivy.google.cloud.bigquery.job.base import _JobReference
from arrivy.google.cloud.bigquery.job.base import ReservationUsage
from arrivy.google.cloud.bigquery.job.base import ScriptStatistics
from arrivy.google.cloud.bigquery.job.base import ScriptStackFrame
from arrivy.google.cloud.bigquery.job.base import TransactionInfo
from arrivy.google.cloud.bigquery.job.base import UnknownJob
from arrivy.google.cloud.bigquery.job.copy_ import CopyJob
from arrivy.google.cloud.bigquery.job.copy_ import CopyJobConfig
from arrivy.google.cloud.bigquery.job.copy_ import OperationType
from arrivy.google.cloud.bigquery.job.extract import ExtractJob
from arrivy.google.cloud.bigquery.job.extract import ExtractJobConfig
from arrivy.google.cloud.bigquery.job.load import LoadJob
from arrivy.google.cloud.bigquery.job.load import LoadJobConfig
from arrivy.google.cloud.bigquery.job.query import _contains_order_by
from arrivy.google.cloud.bigquery.job.query import DmlStats
from arrivy.google.cloud.bigquery.job.query import QueryJob
from arrivy.google.cloud.bigquery.job.query import QueryJobConfig
from arrivy.google.cloud.bigquery.job.query import QueryPlanEntry
from arrivy.google.cloud.bigquery.job.query import QueryPlanEntryStep
from arrivy.google.cloud.bigquery.job.query import ScriptOptions
from arrivy.google.cloud.bigquery.job.query import TimelineEntry
from arrivy.google.cloud.bigquery.enums import Compression
from arrivy.google.cloud.bigquery.enums import CreateDisposition
from arrivy.google.cloud.bigquery.enums import DestinationFormat
from arrivy.google.cloud.bigquery.enums import Encoding
from arrivy.google.cloud.bigquery.enums import QueryPriority
from arrivy.google.cloud.bigquery.enums import SchemaUpdateOption
from arrivy.google.cloud.bigquery.enums import SourceFormat
from arrivy.google.cloud.bigquery.enums import WriteDisposition


# Include classes previously in job.py for backwards compatibility.
__all__ = [
    "_AsyncJob",
    "_error_result_to_exception",
    "_DONE_STATE",
    "_JobConfig",
    "_JobReference",
    "ReservationUsage",
    "ScriptStatistics",
    "ScriptStackFrame",
    "UnknownJob",
    "CopyJob",
    "CopyJobConfig",
    "OperationType",
    "ExtractJob",
    "ExtractJobConfig",
    "LoadJob",
    "LoadJobConfig",
    "_contains_order_by",
    "DmlStats",
    "QueryJob",
    "QueryJobConfig",
    "QueryPlanEntry",
    "QueryPlanEntryStep",
    "ScriptOptions",
    "TimelineEntry",
    "Compression",
    "CreateDisposition",
    "DestinationFormat",
    "Encoding",
    "QueryPriority",
    "SchemaUpdateOption",
    "SourceFormat",
    "TransactionInfo",
    "WriteDisposition",
]
