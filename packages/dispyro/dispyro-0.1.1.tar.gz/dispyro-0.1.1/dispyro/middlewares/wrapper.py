from typing import Any
from .base import BaseMiddleware
from enum import Enum, auto
from contextlib import suppress

class MiddlewareState(Enum):
    UNACTIVE = auto()
    CALLED_ENTER = auto()
    CALLED_EXIT = auto()

class A:
    def __init__(self):
        self._iterable = self.perform()
        self._state = MiddlewareState.UNACTIVE

    async def perform(self):
        print(1)
        yield
        print(2)

    async def __call__(self):
        if self._state is MiddlewareState.UNACTIVE:
            await anext(self._iterable)
            self._state = MiddlewareState.CALLED_ENTER

        elif self._state is MiddlewareState.CALLED_ENTER:
            with suppress(StopAsyncIteration):
                await anext(self._iterable)
            self._state = MiddlewareState.CALLED_EXIT

class MiddlewareCallWrapper:
    def __init__(self, ) -> None:
        self._iterable = middleware()
        self._state = MiddlewareState.UNACTIVE

    async def __call__(self) -> Any:
        pass