from datetime import datetime, tzinfo
from typing import Any

from django.template import Node
from django.template.base import FilterExpression, NodeList, Parser, Token

register: Any

class datetimeobject(datetime): ...

def localtime(value: datetime | str | None) -> Any: ...
def utc(value: datetime | str | None) -> Any: ...
def do_timezone(value: datetime | str | None, arg: tzinfo | str | None) -> Any: ...

class LocalTimeNode(Node):
    nodelist: NodeList
    use_tz: bool
    def __init__(self, nodelist: NodeList, use_tz: bool) -> None: ...

class TimezoneNode(Node):
    nodelist: NodeList
    tz: FilterExpression
    def __init__(self, nodelist: NodeList, tz: FilterExpression) -> None: ...

class GetCurrentTimezoneNode(Node):
    variable: str
    def __init__(self, variable: str) -> None: ...

def localtime_tag(parser: Parser, token: Token) -> LocalTimeNode: ...
def timezone_tag(parser: Parser, token: Token) -> TimezoneNode: ...
def get_current_timezone_tag(parser: Parser, token: Token) -> GetCurrentTimezoneNode: ...