from src.command_abstract import Command
from src.api_services.hunter_api_service import HunterApiService


class DomainSearch(Command):
    """
    A class to represent a domain search command.

    Attributes
    ----------
    domain : str
        The domain you want to find information about.
    command_name : str
        Command name.

    Methods
    -------
    __init__:
    Create a DomainSearch command.

    validate_command_argument:
    Check that a domain is provided in the command argument.

    execute:
    Execute current command.
    """

    domain: str
    command_name = 'domain_search'

    def __init__(self, command_args, storage_service):
        """
        Create a DomainSearch command.

        :param command_args: dict with key 'domain' - {'domain': 'YOUR_DOMAIN'}
        :param storage_service: StorageService type
        """
        super().__init__(command_args, storage_service)
        self.domain = command_args['domain']

    def validate_command_argument(self):
        """
        Check that a domain is provided in the command argument.

        :return:

        Causes an exception if no domain was specified.
        """
        if not self.command_args.get('domain'):
            raise Exception('No email was provided')

    def execute(self):
        """
        Execute current command.

        :return:

        Return all the email addresses found using one given domain name, with sources.
        """
        response = HunterApiService().domain_search(self.domain)
        print({'command': self.command_name, 'status': 'success', 'data': response})
        return {'command': self.command_name, 'status': 'success', 'data': response}
