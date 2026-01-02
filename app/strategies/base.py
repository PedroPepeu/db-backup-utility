from abc import ABC, abstractmethod


class DatabaseStrategy(ABC):
    """
    Abstract class that defines the contract to any backup strategies.
    """

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def backup(self) -> str | None:
        """
        Must be implemented by all subclasses.

        Process: Realize the backup
        Return: The path of the file generated
        """
        pass
