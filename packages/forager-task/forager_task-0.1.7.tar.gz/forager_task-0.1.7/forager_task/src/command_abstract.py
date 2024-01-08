from abc import ABC, abstractmethod

from src.storage_service_abstract import StorageService


class Command(ABC):
    """
    An abstract class Command.

    Attributes
    ----------
    command_args : dict
        Command arguments what depends on kind of command.
    storage_service : StorageService
        Type of storage service what will be used (SQLite, JSON).

    Methods
    -------
    __init__: Create an abstract Command.
    validate_command_argument: Abstract method to validate command argument.
    execute: Abstract method to execute command.
    """

    command_args: dict
    storage_service: StorageService

    def __init__(self, command_args, storage_service):
        """
        Create an abstract Command.

        :param command_args: Command arguments what depends on kind of command.
        :param storage_service: Type of storage service what will be used (SQLite, JSON).
        """
        self.command_args = command_args
        self.storage_service = storage_service
        self.validate_command_argument()

    @abstractmethod
    def validate_command_argument(self):
        """
        Abstract method to validate command argument.

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        """
        Abstract method to execute command.

        :return:
        """
        raise NotImplementedError
