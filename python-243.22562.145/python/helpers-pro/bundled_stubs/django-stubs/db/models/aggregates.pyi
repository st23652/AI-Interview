from typing import Any, ClassVar

from django.db.models.expressions import Func
from django.db.models.fields import IntegerField
from django.db.models.functions.mixins import FixDurationInputMixin, NumericOutputFieldMixin

class Aggregate(Func):
    filter_template: str
    filter: Any
    allow_distinct: bool
    empty_result_set_value: int | None
    def __init__(self, *expressions: Any, distinct: bool = ..., filter: Any | None = ..., **extra: Any) -> None: ...

class Avg(FixDurationInputMixin, NumericOutputFieldMixin, Aggregate): ...

class Count(Aggregate):
    output_field: ClassVar[IntegerField]

class Max(Aggregate): ...
class Min(Aggregate): ...
class StdDev(NumericOutputFieldMixin, Aggregate): ...
class Sum(FixDurationInputMixin, Aggregate): ...
class Variance(NumericOutputFieldMixin, Aggregate): ...
