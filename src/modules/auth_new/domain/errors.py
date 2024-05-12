from core_new.domain.errors import DBError, DomainError


class UserNotFound(DBError): pass


class BadCredentials(DomainError): pass
