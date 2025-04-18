from collections.abc import Callable, Sequence
from typing import Any, Literal

from django.http.response import HttpResponse
from django.urls.resolvers import ResolverMatch

def resolve(path: str, urlconf: str | None = ...) -> ResolverMatch: ...
def reverse(
    viewname: Callable[..., HttpResponse] | str | None,
    urlconf: str | None = ...,
    args: Sequence[Any] | None = ...,
    kwargs: dict[str, Any] | None = ...,
    current_app: str | None = ...,
) -> str: ...

reverse_lazy: Any

def clear_url_caches() -> None: ...
def set_script_prefix(prefix: str) -> None: ...
def get_script_prefix() -> str: ...
def clear_script_prefix() -> None: ...
def set_urlconf(urlconf_name: str | None) -> None: ...
def get_urlconf(default: str | None = ...) -> str | None: ...
def is_valid_path(path: str, urlconf: str | None = ...) -> Literal[False] | ResolverMatch: ...
def translate_url(url: str, lang_code: str) -> str: ...
