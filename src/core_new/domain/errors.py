from http import HTTPStatus


class Error(Exception):
    MESSAGE = "Something went wrong"
    STATUS_CODE = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message=None, status_code: HTTPStatus | None = None):
        self.message = message or self.MESSAGE
        self.status_code = status_code or self.STATUS_CODE
        super().__init__(self.message)


class DomainError(Error):
    STATUS_CODE = HTTPStatus.BAD_REQUEST


class DBError(Error): ...


class DBErrorNotFound(DBError):
    STATUS_CODE = HTTPStatus.NOT_FOUND
