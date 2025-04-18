from typing import Any

from django.core.signals import setting_changed as setting_changed

template_rendered: Any
COMPLEX_OVERRIDE_SETTINGS: Any

def clear_cache_handlers(*, setting: str, **kwargs: Any) -> None: ...
def update_installed_apps(*, setting: str, **kwargs: Any) -> None: ...
def update_connections_time_zone(*, setting: str, **kwargs: Any) -> None: ...
def clear_routers_cache(*, setting: str, **kwargs: Any) -> None: ...
def reset_template_engines(*, setting: str, **kwargs: Any) -> None: ...
def storages_changed(*, setting: str, **kwargs: Any) -> None: ...
def clear_serializers_cache(*, setting: str, **kwargs: Any) -> None: ...
def language_changed(*, setting: str, **kwargs: Any) -> None: ...
def localize_settings_changed(*, setting: str, **kwargs: Any) -> None: ...
def file_storage_changed(*, setting: str, **kwargs: Any) -> None: ...
def complex_setting_changed(*, setting: str, enter: bool, **kwargs: Any) -> None: ...
def root_urlconf_changed(*, setting: str, **kwargs: Any) -> None: ...
def static_storage_changed(*, setting: str, **kwargs: Any) -> None: ...
def static_finders_changed(*, setting: str, **kwargs: Any) -> None: ...
def auth_password_validators_changed(*, setting: str, **kwargs: Any) -> None: ...
def user_model_swapped(*, setting: str, **kwargs: Any) -> None: ...
