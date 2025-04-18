from collections.abc import Callable

from django.apps.registry import Apps
from django.db.models.base import Model
from django.dispatch import Signal

class_prepared: Signal

class ModelSignal(Signal):
    def connect(  # type: ignore[override]
        self,
        receiver: Callable,
        sender: type[Model] | str | None = ...,
        weak: bool = ...,
        dispatch_uid: str | None = ...,
        apps: Apps | None = ...,
    ) -> None: ...
    def disconnect(  # type: ignore[override]
        self,
        receiver: Callable | None = ...,
        sender: type[Model] | str | None = ...,
        dispatch_uid: str | None = ...,
        apps: Apps | None = ...,
    ) -> bool | None: ...

pre_init: ModelSignal
post_init: ModelSignal
pre_save: ModelSignal
post_save: ModelSignal
pre_delete: ModelSignal
post_delete: ModelSignal
m2m_changed: ModelSignal
pre_migrate: Signal
post_migrate: Signal
