from abc import ABCMeta

from src.core.domain.repo import IRepository


class IUserRepo(IRepository, metaclass=ABCMeta):
    pass
