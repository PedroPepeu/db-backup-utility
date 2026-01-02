from abc import ABC, abstractmethod


class StorageStrategy(ABC):
    @abstractmethod
    def save(self, source_path: str, destination_filename: str) -> None:
        """
        Save 'source_path' in the destiny.
        """
        pass
