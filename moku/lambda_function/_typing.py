from typing import Callable, Dict
from dataclasses import dataclass

DefaultLambdaHandler = Callable[[dict], dict]
CustomEventMap = Dict[str, DefaultLambdaHandler]


@dataclass
class DefaultCustomEventAction:
    name: str
    action: DefaultLambdaHandler
