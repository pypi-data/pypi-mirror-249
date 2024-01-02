class JarvisInternalException(Exception):
    def __init__(
            self,
            message: str
    ) -> None:
        self.message = message


class JarvisNotFoundException(Exception):
    def __init__(
            self,
            message: str
    ) -> None:
        self.message = message
