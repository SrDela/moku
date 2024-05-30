from dataclasses import dataclass
from typing import Callable

ObjectProcessor = Callable[[any], None]


@dataclass
class ExtensionProcessor:
    extension: str
    func: ObjectProcessor
