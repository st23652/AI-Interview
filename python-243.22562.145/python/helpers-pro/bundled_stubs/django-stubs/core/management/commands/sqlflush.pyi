from typing import Any

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    output_transaction: bool

    def handle(self, **options: Any) -> str: ...
