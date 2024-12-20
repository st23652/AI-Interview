from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.fields import CharField, EmailField, TextField

class CIText:
    def get_internal_type(self) -> str: ...
    def db_type(self, connection: BaseDatabaseWrapper) -> str: ...

class CICharField(CIText, CharField): ...
class CIEmailField(CIText, EmailField): ...
class CITextField(CIText, TextField): ...