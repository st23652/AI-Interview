from datetime import tzinfo
from typing import Any, ClassVar

from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Func, Transform
from django.db.models.expressions import Combinable
from django.db.models.fields import Field
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType

class TimezoneMixin:
    tzinfo: Any
    def get_tzname(self) -> str | None: ...

class Extract(TimezoneMixin, Transform):
    lookup_name: str
    output_field: ClassVar[models.IntegerField]
    def __init__(
        self, expression: Combinable | str, lookup_name: str | None = ..., tzinfo: Any | None = ..., **extra: Any
    ) -> None: ...

class ExtractYear(Extract): ...
class ExtractIsoYear(Extract): ...
class ExtractMonth(Extract): ...
class ExtractDay(Extract): ...
class ExtractWeek(Extract): ...
class ExtractWeekDay(Extract): ...
class ExtractIsoWeekDay(Extract): ...
class ExtractQuarter(Extract): ...
class ExtractHour(Extract): ...
class ExtractMinute(Extract): ...
class ExtractSecond(Extract): ...

class Now(Func):
    output_field: ClassVar[models.DateTimeField]

    def as_oracle(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...

class TruncBase(TimezoneMixin, Transform):
    kind: str
    tzinfo: Any

    def __init__(
        self, expression: Combinable | str, output_field: Field | None = ..., tzinfo: tzinfo | None = ..., **extra: Any
    ) -> None: ...
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...  # type: ignore[override]

class Trunc(TruncBase):
    def __init__(
        self,
        expression: Combinable | str,
        kind: str,
        output_field: Field | None = ...,
        tzinfo: tzinfo | None = ...,
        **extra: Any,
    ) -> None: ...

class TruncYear(TruncBase): ...
class TruncQuarter(TruncBase): ...
class TruncMonth(TruncBase): ...
class TruncWeek(TruncBase): ...
class TruncDay(TruncBase): ...

class TruncDate(TruncBase):
    output_field: ClassVar[models.DateField]

class TruncTime(TruncBase):
    output_field: ClassVar[models.TimeField]

class TruncHour(TruncBase): ...
class TruncMinute(TruncBase): ...
class TruncSecond(TruncBase): ...
