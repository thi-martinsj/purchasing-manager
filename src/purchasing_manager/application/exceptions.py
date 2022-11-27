class ConfigurationNotValid(Exception):
    pass


class DatabaseException(Exception):
    def __init__(self, *args: object, status: int = 500) -> None:
        super().__init__(*args)
        self.status = status
