

class BaseError(Exception):
    def __init__(self, reason: str):
        self.reason = reason

    def get_reason(self) -> str:
        return self.reason

    def to_string(self) -> str:
        return f"{self.__class__.__name__} - {self.reason}"

    def __str__(self) -> str:
        return self.to_string()
