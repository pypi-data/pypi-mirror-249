from contextlib import ContextDecorator
from contextvars import Token

from .settings import versioning_is_disabled


class disabled_versioning(ContextDecorator):
    def __init__(self):
        self._context_token: Token | None = None

    def __enter__(self):
        self._context_token = versioning_is_disabled.set(True)
        return self

    def __exit__(self, *exc):
        assert self._context_token is not None, f"Context token is not set"
        versioning_is_disabled.reset(self._context_token)
        self._context_token = None
        return False
