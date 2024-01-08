from src.command_abstract import Command
from src.api_services.hunter_api_service import HunterApiService


class EmailVerification(Command):
    """
    A class to represent a email verification command.

    Attributes
    ----------
    email : str
        The email you want to verify.
    command_name : str
        Command name.

    Methods
    -------
    __init__:
    Create a EmailVerification command.

    validate_command_argument:
    Check that an email is provided in the command argument.

    execute:
    Execute current command.
    """

    email: str
    command_name = 'email_verification'

    def __init__(self, command_args, storage_service):
        """
        Create a EmailVerification command.

        :param command_args: dict with key 'email' - {'email': 'YOUR_EMAIL'}
        :param storage_service: StorageService type
        """
        super().__init__(command_args, storage_service)
        self.email = command_args['email']

    def validate_command_argument(self):
        """
        Check that an email is provided in the command argument.

        :return:

        Causes an exception if no email was specified.
        """
        if not self.command_args.get('email'):
            raise Exception('No email was provided')

    def execute(self):
        """
        Execute current command.

        :return:

        Saved response in your storage, what was defined in the save_strategy and return the status of your request.
        """
        response = HunterApiService().email_verify(self.email)
        self.storage_service.add_record(response)
        print({'command': self.command_name, 'status': 'success', 'data': response})
        return {'command': self.command_name, 'status': 'success', 'data': response}
