class HandlerNotFoundError(RuntimeError):
    def __init__(self, *args):  # type: (object) -> None
        super().__init__(args)
