from typing import Callable, Dict


RouteAction = Callable[[dict], any]
RouteActionList = Dict[str, RouteAction]
