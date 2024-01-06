"""Verify email using hunter."""
from typing import Dict, Union

import requests


class EmailVerificationClient:
    """Verify email using hunter."""
    def __init__(self, api_key: str):
        """Initialize the client."""
        self.api_key = api_key
        self.base_url = "https://api.hunter.io/v2/"

    def verify_email(self, email: str) -> Dict[str, Union[str, bool]]:
        """Verify email using hunter."""
        endpoint = f"email-verifier?email={email}&api_key={self.api_key}"
        response = requests.get(self.base_url + endpoint)
        response_data = response.json()

        if response.status_code == 200:
            return {'email': email, 'verification_result': response_data['data']['result']}
        return {'email': email, 'verification_result': f'Error: {response_data["errors"][0]["details"]}'}
