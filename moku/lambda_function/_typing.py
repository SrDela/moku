from typing import Callable, Dict
from moku._interfaces.event_source import EventSource
from moku._interfaces.event_handler import EventHandler


DefaultLambdaHandler = Callable[[dict], dict]
TriggerMap = Dict[EventSource, EventHandler]