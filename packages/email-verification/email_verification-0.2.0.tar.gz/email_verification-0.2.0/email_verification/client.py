"""Verify email using hunter."""
from typing import Dict, Union

import requests


class EmailVerificationClient(object):
    """Verify email using hunter."""

    http_ok = 200

    def __init__(self, api_key: str):
        """Initialize the client."""
        self.api_key = api_key
        self.base_url = 'https://api.hunter.io/v2/'

    def verify_email(self, email: str) -> Dict[str, Union[str, bool]]:
        """Verify email using hunter."""
        endpoint = 'email-verifier?email={email}&api_key={api_key}'.format(email=email, api_key=self.api_key)
        response = requests.get(self.base_url + endpoint, timeout=100)
        response_data = response.json()

        if response.status_code == self.http_ok:
            return {
                'email': email,
                'verification_result': response_data['data']['result'],
            }
        return {
            'email': email,
            'verification_result': 'Error: {response_data}'.format(response_data=response_data['errors'][0]['details']),
        }
