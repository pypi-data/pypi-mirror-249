from src.commands.email_verification_command import EmailVerification
from src.commands.domain_search_command import DomainSearch
from src.commands.get_record_command import GetRecordCommand
from src.commands.delete_record_command import DeleteRecordCommand
from src.services.storage_service_sqlite import SQLiteSaveService
from src.services.storage_service_json import JSONSaveService
from src.storage_service_abstract import StorageService
from src.command_abstract import Command


class SaveFactory:
    """
    A class SaveFactory.

    Method
    -------
    get_save_service:  Determine which type of storage service will be used.
    """

    @staticmethod
    def get_save_service(save_strategy: str) -> StorageService:
        """
        Determine which type of storage service will be used.

        :param save_strategy: Type of storage service ('to_db', 'to_file').
        :return: Type of storage service what will be used (SQLiteSaveService, JSONSaveService).
        """
        if save_strategy == 'to_db':
            return SQLiteSaveService()
        elif save_strategy == 'to_file':
            return JSONSaveService()
        else:
            raise Exception('Not supported retailer')


class CommandFactory:
    """
    A class Command.

    Method
    -------
    get_task: Determine which command will be executed and with what parameters.
    """

    @staticmethod
    def get_task(command: str, command_args: dict, storage_service: StorageService) -> Command:
        """
        Determine which command will be executed and with what parameters.

        :param command: Type of command.
        :param command_args: Parameters what needed for current command.
        :param storage_service: Type of storage service what will be used with current command.
        :return:
        """
        if command == 'email_verification':
            return EmailVerification(command_args, storage_service)
        elif command == 'domain_search':
            return DomainSearch(command_args, storage_service)
        elif command == 'get_record':
            return GetRecordCommand(command_args, storage_service)
        elif command == 'delete_record':
            return DeleteRecordCommand(command_args, storage_service)
        else:
            raise Exception('Not supported retailer')
