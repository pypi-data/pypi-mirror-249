# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Google BigQuery implementation of the Database API Specification v2.0.

This module implements the `Python Database API Specification v2.0 (DB-API)`_
for Google BigQuery.

.. _Python Database API Specification v2.0 (DB-API):
   https://www.python.org/dev/peps/pep-0249/
"""

from arrivy.google.cloud.bigquery.dbapi.connection import connect
from arrivy.google.cloud.bigquery.dbapi.connection import Connection
from arrivy.google.cloud.bigquery.dbapi.cursor import Cursor
from arrivy.google.cloud.bigquery.dbapi.exceptions import Warning
from arrivy.google.cloud.bigquery.dbapi.exceptions import Error
from arrivy.google.cloud.bigquery.dbapi.exceptions import InterfaceError
from arrivy.google.cloud.bigquery.dbapi.exceptions import DatabaseError
from arrivy.google.cloud.bigquery.dbapi.exceptions import DataError
from arrivy.google.cloud.bigquery.dbapi.exceptions import OperationalError
from arrivy.google.cloud.bigquery.dbapi.exceptions import IntegrityError
from arrivy.google.cloud.bigquery.dbapi.exceptions import InternalError
from arrivy.google.cloud.bigquery.dbapi.exceptions import ProgrammingError
from arrivy.google.cloud.bigquery.dbapi.exceptions import NotSupportedError
from arrivy.google.cloud.bigquery.dbapi.types import Binary
from arrivy.google.cloud.bigquery.dbapi.types import Date
from arrivy.google.cloud.bigquery.dbapi.types import DateFromTicks
from arrivy.google.cloud.bigquery.dbapi.types import Time
from arrivy.google.cloud.bigquery.dbapi.types import TimeFromTicks
from arrivy.google.cloud.bigquery.dbapi.types import Timestamp
from arrivy.google.cloud.bigquery.dbapi.types import TimestampFromTicks
from arrivy.google.cloud.bigquery.dbapi.types import BINARY
from arrivy.google.cloud.bigquery.dbapi.types import DATETIME
from arrivy.google.cloud.bigquery.dbapi.types import NUMBER
from arrivy.google.cloud.bigquery.dbapi.types import ROWID
from arrivy.google.cloud.bigquery.dbapi.types import STRING


apilevel = "2.0"

# Threads may share the module and connections, but not cursors.
threadsafety = 2

paramstyle = "pyformat"

__all__ = [
    "apilevel",
    "threadsafety",
    "paramstyle",
    "connect",
    "Connection",
    "Cursor",
    "Warning",
    "Error",
    "InterfaceError",
    "DatabaseError",
    "DataError",
    "OperationalError",
    "IntegrityError",
    "InternalError",
    "ProgrammingError",
    "NotSupportedError",
    "Binary",
    "Date",
    "DateFromTicks",
    "Time",
    "TimeFromTicks",
    "Timestamp",
    "TimestampFromTicks",
    "BINARY",
    "DATETIME",
    "NUMBER",
    "ROWID",
    "STRING",
]
