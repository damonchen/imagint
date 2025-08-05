class BaseServiceError(Exception):
    def __init__(self, description: str | None = None) -> None:
        super(BaseException, self).__init__()
        self.description = description
