import typing as t
from contextvars import ContextVar

from django.conf import settings

DEFAULT_VERSION: t.Final[int] = getattr(settings, "DEFAULT_VERSION", 0)
versioning_is_disabled: ContextVar[bool] = ContextVar("versioning_is_disabled", default=False)
