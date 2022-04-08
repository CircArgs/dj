"""
An implementation of the DB API 2.0.
"""
# pylint: disable=invalid-name, redefined-builtin

from datajunction.sql.dbapi.connection import connect
from datajunction.sql.dbapi.exceptions import (
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Warning,
)
from datajunction.sql.dbapi.types import (
    BINARY,
    DATETIME,
    NUMBER,
    STRING,
    Binary,
    Date,
    DateFromTicks,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
)

apilevel = "2.0"
threadsafety = 3
paramstyle = "pyformat"
