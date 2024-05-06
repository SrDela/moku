from typing import Dict, Callable, Optional
from dataclasses import dataclass, field


RouteAction = Callable[[dict], any]


@dataclass
class RouteProps:
    action: Optional[str] = field(default="")
    id_: Optional[str] = field(default="")
    methods: Dict[str, RouteAction] = field(default_factory=dict)


RouteMap = Dict[str, RouteProps]
