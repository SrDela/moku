from abc import ABC


class EventHandler(ABC):

    def resolve(self, *args: any, **kwargs: any) -> dict:
        raise NotImplementedError
