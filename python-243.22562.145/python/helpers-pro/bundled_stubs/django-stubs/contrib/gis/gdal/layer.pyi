from collections.abc import Iterator
from typing import Any, AnyStr, Literal, overload

from django.contrib.gis.gdal.base import GDALBase
from django.contrib.gis.gdal.envelope import Envelope
from django.contrib.gis.gdal.feature import Feature
from django.contrib.gis.gdal.field import Field
from django.contrib.gis.gdal.geometries import OGRGeometry
from django.contrib.gis.gdal.geomtype import OGRGeomType
from django.contrib.gis.gdal.srs import SpatialReference
from django.contrib.gis.geos.geometry import GEOSGeometry

class Layer(GDALBase):
    ptr: Any
    def __init__(self, layer_ptr: Any, ds: Any) -> None: ...
    @overload
    def __getitem__(self, index: int) -> Feature: ...
    @overload
    def __getitem__(self, index: slice) -> list[Feature]: ...
    def __iter__(self) -> Iterator[Feature]: ...
    def __len__(self) -> int: ...
    @property
    def extent(self) -> Envelope: ...
    @property
    def name(self) -> str: ...
    @property
    def num_feat(self) -> int: ...
    @property
    def num_fields(self) -> int: ...
    @property
    def geom_type(self) -> OGRGeomType: ...
    @property
    def srs(self) -> SpatialReference: ...
    @property
    def fields(self) -> list[str]: ...
    @property
    def field_types(self) -> list[type[Field]]: ...
    @property
    def field_widths(self) -> list[int]: ...
    @property
    def field_precisions(self) -> list[int]: ...
    spatial_filter: OGRGeometry | None
    def get_fields(self, field_name: str) -> list[Any]: ...
    @overload
    def get_geoms(self, geos: Literal[False] = ...) -> list[OGRGeometry]: ...
    @overload
    def get_geoms(self, geos: Literal[True]) -> list[GEOSGeometry]: ...
    def test_capability(self, capability: AnyStr) -> bool: ...
