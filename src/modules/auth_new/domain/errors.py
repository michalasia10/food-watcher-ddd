from http import HTTPStatus

from src.core_new.domain.errors import DBErrorNotFound, DomainError


class UserNotFound(DBErrorNotFound): ...


class BadCredentials(DomainError):
    STATUS_CODE = HTTPStatus.UNAUTHORIZED


class InvalidToken(DomainError):
    STATUS_CODE = HTTPStatus.UNAUTHORIZED
