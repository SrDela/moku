from __future__ import annotations
from typing import Optional
from inspect import ismethod, isfunction

from . import _typing
from .exceptions import InvalidExtensionError, InvalidProcessorError


class ExtensionProcessorBuilder:

    def __init__(self, ext: Optional[str] = None) -> None:
        self.__ext: Optional[str] = ext

    @staticmethod
    def bind(ext: str) -> ExtensionProcessorBuilder:
        return ExtensionProcessorBuilder(ext)

    def to(self, func: _typing.ObjectProcessor) -> _typing.ExtensionProcessor:
        if self.__ext is None:
            raise InvalidExtensionError("Looks like an extension has not been set up. Make sure to call the 'bind' method.")
        if not isfunction(func) and not ismethod(func):
            raise InvalidProcessorError("'func' must be a function or method.")
        return _typing.ExtensionProcessor(extension=self.__ext, func=func)
