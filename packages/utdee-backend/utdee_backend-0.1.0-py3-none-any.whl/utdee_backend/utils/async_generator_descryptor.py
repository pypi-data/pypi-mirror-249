from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Iterable


class AsyncGeneratorDescriptor:

    def __set_name__(self, owner, name):
        self._private_name = "_" + name

    def __get__(self, instance, owner) -> AsyncGenerator:
        return self._generator(instance)

    def __set__(self, instance, value: Iterable):
        setattr(instance, self._private_name, value)

    async def _generator(self, instance):
        for i in getattr(instance, self._private_name):
            yield i


async def async_generator(samples):
    for i in range(samples):
        yield i
