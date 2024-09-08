from http import HTTPStatus

from src.core.domain.errors import DBErrorNotFound, DomainError, BadPermissions


class UserNotFound(DBErrorNotFound): ...


class UserSettingsNotFound(DBErrorNotFound): ...


class UserNotRecordOwner(BadPermissions): ...


class BadCredentials(DomainError):
    STATUS_CODE = HTTPStatus.UNAUTHORIZED


class InvalidToken(DomainError):
    STATUS_CODE = HTTPStatus.UNAUTHORIZED
