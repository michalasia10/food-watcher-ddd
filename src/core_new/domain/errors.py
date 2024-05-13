class Error(Exception):
    MESSAGE = "Something went wrong"
    STATUS_CODE = 500

    def __init__(self, message=None, status_code=None):
        self.message = message or self.MESSAGE
        self.status_code = status_code or self.STATUS_CODE
        super().__init__(self.message)


class DomainError(Error):
    STATUS_CODE = 400


class DBError(Error): ...
