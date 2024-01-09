"""Verify email using hunter."""
from typing import Dict, Optional
from urllib.parse import urlencode, urljoin

import requests


class EmailVerificationClient(object):
    """Verify email using hunter."""

    http_ok = 200

    def __init__(self, api_key: str, timeout: int = 2) -> None:
        """Initialize the client."""
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = 'https://api.hunter.io/v2/'

    def verify_email(self, email: str) -> Dict[str, str]:
        """Verify email using hunter."""
        request_params = {'email': email}
        url = self._url_builder('email-verifier', request_params)
        response_data = self._make_request(url)
        return response_data.json()

    def count_emails(self, domain: str, company: str = None, email_type: str = None):
        """Count all emails using hunter."""
        request_params = {'domain': domain, 'company': company, 'email_type': email_type}
        url = self._url_builder('email-count', request_params)
        response_data = self._make_request(url)
        return response_data.json()

    def _url_builder(self, url: str, request_params: Dict[str, Optional[str]]) -> str:
        """Build url using urllib and format."""
        request_params['api_key'] = self.api_key
        request_params = {key: entered_param for key, entered_param in request_params.items() if entered_param}
        request_params = urlencode(request_params)
        endpoint = '{request_url}?{request_params}'.format(request_url=url, request_params=request_params)
        return urljoin(self.base_url, endpoint)

    def _make_request(self, request_url: str) -> requests.Response:
        """Make a request to hunters."""
        response = requests.get(request_url, timeout=self.timeout)
        if response.status_code != self.http_ok:
            response.raise_for_status()
        return response
