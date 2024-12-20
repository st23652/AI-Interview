from typing import Any

from .base import GEOSBase
from .geometry import GEOSGeometry

class PreparedGeometry(GEOSBase):
    ptr_type: Any
    destructor: Any
    ptr: Any
    def __init__(self, geom: Any) -> None: ...
    def contains(self, other: GEOSGeometry) -> bool: ...
    def contains_properly(self, other: GEOSGeometry) -> bool: ...
    def covers(self, other: GEOSGeometry) -> bool: ...
    def intersects(self, other: GEOSGeometry) -> bool: ...
    def crosses(self, other: GEOSGeometry) -> bool: ...
    def disjoint(self, other: GEOSGeometry) -> bool: ...
    def overlaps(self, other: GEOSGeometry) -> bool: ...
    def touches(self, other: GEOSGeometry) -> bool: ...
    def within(self, other: GEOSGeometry) -> bool: ...