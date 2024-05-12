from abc import ABCMeta

from core_new.domain.repo import IRepository


class IUserRepo(IRepository, metaclass=ABCMeta):
    pass
