class InvalidExtensionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidProcessorError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)