import json
import requests

from config import HUNTER_API_KEY


class HunterApiService:
    """
    A class to represent an API service https://hunter.io.

    Attributes
    ----------
    api_key : str
        Your secret API key. You can generate it in https://hunter.io.
    email_url : str
        URL to make request for email_verification.
    domain_url : str
        URL to make request for domain search.

    Methods
    -------
    email_verify:

    domain_search:
    """

    api_key = HUNTER_API_KEY
    email_url = 'https://api.hunter.io/v2/email-verifier'
    domain_url = 'https://api.hunter.io/v2/domain-search'

    def email_verify(self, email: str) -> dict:
        """
        Make a GET request to the https://api.hunter.io/v2/email-verifier, .

        :param email:

        {'email': 'YOUR_EMAIL', 'api_key': 'YOUR_SECRET_API_KEY'}

        :return:

        Check the deliverability and verify the email , return their sources.
        """
        response = requests.get(self.email_url, params={'email': email, 'api_key': self.api_key})
        return json.loads(response.text)['data']

    def domain_search(self, domain: str) -> dict:
        """
        Make a GET request to the https://api.hunter.io/v2/domain-search.

        :param domain:

        {'domain': 'YOUR_DOMAIN', 'api_key': 'YOUR_SECRET_API_KEY'}.

        :return:

        Return all the email addresses found using one given domain name.

        """
        response = requests.get(self.domain_url, params={'domain': domain, 'api_key': self.api_key})
        return json.loads(response.text)['data']
