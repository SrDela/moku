class InvalidCustomEventAction(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DuplicatedEventHandlerError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidCustomEventError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
