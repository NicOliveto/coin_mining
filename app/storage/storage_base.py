from abc import ABC, abstractmethod

class StorageBase(ABC):
    @abstractmethod
    def save(self, data: list):
        pass
