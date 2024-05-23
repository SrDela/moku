from dataclasses import dataclass
from typing import Callable


AuthorizationProcedure = Callable[[dict], any]


@dataclass
class AuthorizerType:
    type: str
    procedure: AuthorizationProcedure
