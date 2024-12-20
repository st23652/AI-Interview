from typing import Any

def get_type_oids(connection_alias: str, type_name: str) -> tuple[tuple[Any, ...], tuple[Any, ...]]: ...
def get_hstore_oids(connection_alias: str) -> tuple[tuple[Any, ...], tuple[Any, ...]]: ...
def get_citext_oids(connection_alias: str) -> tuple[tuple[Any, ...], tuple[Any, ...]]: ...
def register_type_handlers(connection: Any, **kwargs: Any) -> None: ...