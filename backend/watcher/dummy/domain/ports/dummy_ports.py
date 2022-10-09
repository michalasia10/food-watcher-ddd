from abc import ABC, abstractmethod


class ListUser(ABC):

    @abstractmethod
    def all(self) -> dict:
        pass
