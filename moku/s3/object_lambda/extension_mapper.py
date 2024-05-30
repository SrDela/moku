from typing import Dict

from . import _typing
from .exceptions import InvalidExtensionError


class ExtensionMapper:

    def __init__(self) -> None:
        self.__ext_map: Dict[str, _typing.ObjectProcessor] = {}

    def add_extension(self, processor: _typing.ExtensionProcessor) -> None:
        if self.__ext_map.get(processor.extension) is not None:
            raise InvalidExtensionError('Already mapped.')
        self.__ext_map[processor.extension] = processor.func

    def resolve(self, extension: str) -> _typing.ObjectProcessor:
        if self.__ext_map.get(extension) is None:
            raise InvalidExtensionError('Extension is not mapped.')
        return self.__ext_map[extension]
