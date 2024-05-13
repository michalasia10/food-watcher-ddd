from core_new.domain.errors import DBError, DomainError


class UserNotFound(DBError): pass


class BadCredentials(DomainError):
    STATUS_CODE = 401


class InvalidToken(DomainError):
    STATUS_CODE = 401
