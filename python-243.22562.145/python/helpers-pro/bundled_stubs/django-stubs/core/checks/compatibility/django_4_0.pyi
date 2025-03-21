from collections.abc import Sequence
from typing import Any

from django.apps.config import AppConfig
from django.core.checks.messages import Error

def check_csrf_trusted_origins(app_configs: Sequence[AppConfig] | None, **kwargs: Any) -> list[Error]: ...
