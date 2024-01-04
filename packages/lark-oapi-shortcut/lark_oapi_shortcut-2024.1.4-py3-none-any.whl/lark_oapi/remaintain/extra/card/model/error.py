class HandlerNotFoundError(RuntimeError):
    def __init__(self, *args):  # type: (object) -> None
        super().__init__(args)


class SignatureError(RuntimeError):
    def __init__(self, *args):  # type: (object) -> None
        super().__init__(args)


class TokenInvalidError(RuntimeError):
    def __init__(self, *args):  # type: (object) -> None
        super().__init__(args)
