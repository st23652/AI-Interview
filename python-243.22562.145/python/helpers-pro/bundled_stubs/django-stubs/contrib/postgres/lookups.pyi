from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Transform
from django.db.models.lookups import PostgresOperatorLookup
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType

from .search import SearchVectorExact

class DataContains(PostgresOperatorLookup): ...
class ContainedBy(PostgresOperatorLookup): ...
class Overlap(PostgresOperatorLookup): ...
class HasKey(PostgresOperatorLookup): ...
class HasKeys(PostgresOperatorLookup): ...
class HasAnyKeys(HasKeys): ...
class Unaccent(Transform): ...

class SearchLookup(SearchVectorExact):
    def process_lhs(self, qn: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...  # type: ignore[override]

class TrigramSimilar(PostgresOperatorLookup): ...
class TrigramWordSimilar(PostgresOperatorLookup): ...
class TrigramStrictWordSimilar(PostgresOperatorLookup): ...