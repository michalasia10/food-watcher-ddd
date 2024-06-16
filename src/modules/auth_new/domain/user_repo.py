from abc import ABCMeta

from src.core_new.domain.repo import IRepository


class IUserRepo(IRepository, metaclass=ABCMeta):
    pass
