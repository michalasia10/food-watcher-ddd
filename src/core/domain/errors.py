from http import HTTPStatus

from loguru import logger


class Error(Exception):
    MESSAGE = "Something went wrong"
    STATUS_CODE = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message=None, status_code: HTTPStatus | None = None):
        self.message = message or self.MESSAGE
        self.status_code = status_code or self.STATUS_CODE
        super().__init__(self.message)
        logger.info(
            "[{class_name}] | {message} ",
            class_name=self.__class__.__name__,
            message=self.message,
            status_code=self.status_code,
        )


class DomainError(Error):
    STATUS_CODE = HTTPStatus.BAD_REQUEST


class ValidationError(DomainError):
    STATUS_CODE = HTTPStatus.BAD_REQUEST


class DBError(Error): ...


class DBErrorNotFound(DBError):
    STATUS_CODE = HTTPStatus.NOT_FOUND


class BadPermissions(DomainError):
    STATUS_CODE = HTTPStatus.FORBIDDEN
