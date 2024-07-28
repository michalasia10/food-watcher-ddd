from abc import ABCMeta

from src.core.domain.repo.postgres import IPostgresRepository


class IUserRepo(IPostgresRepository, metaclass=ABCMeta):
    pass
