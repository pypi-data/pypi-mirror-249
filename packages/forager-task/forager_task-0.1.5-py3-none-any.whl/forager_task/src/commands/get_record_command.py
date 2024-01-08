from src.command_abstract import Command


class GetRecordCommand(Command):
    """
    A class to represent a ger record command.

    Attributes
    ----------
    email : str
        The email what you want to get from your storage.
    command_name : str
        Command name.

    Methods
    -------
    __init__:
    Create a GetRecordCommand.

    validate_command_argument:
    Check that an email address is provided in the command argument.

    execute:
    Execute current command and get information about current email from your storage.
    """

    email: str
    command_name = 'get_records'

    def __init__(self, command_args, storage_service):
        """
        Create a GetRecordCommand.

        :param command_args: dict with key 'email' - {'email': 'YOUR_EMAIL'}
        :param storage_service: StorageService type
        """
        super().__init__(command_args, storage_service)
        self.email = command_args['email']

    def validate_command_argument(self):
        """
        Check that an email address is provided in the command argument.

        :return:

        Causes an exception if no email was specified.
        """
        if not self.command_args.get('email'):
            raise Exception('No email was provided')

    def execute(self):
        """
        Execute current command and get information about current email from your storage.

        :return:

        Return the dict with the status of execution.
        """
        response = self.storage_service.get_record(self.email)
        print({'command': self.command_name, 'status': 'success', 'data': response})
        return {'command': self.command_name, 'status': 'success', 'data': response}
