"""Verify email using hunter."""
from typing import Dict
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

    def make_request(self, endpoint: str, **kwargs: str) -> Dict[str, str]:
        """Make a generic request using hunter."""
        url = self._url_builder(endpoint, **kwargs)
        response_data = self._make_request(url)
        return response_data.json()

    def _url_builder(self, url: str, **kwargs: str) -> str:
        """Build url using urllib and format."""
        kwargs['api_key'] = self.api_key
        filtered_params = {key: request_param for key, request_param in kwargs.items() if request_param}
        encoded_params = urlencode(filtered_params)
        full_url = '{base_url}{endpoint}?{params}'.format(
            base_url=self.base_url,
            endpoint=url,
            params=encoded_params,
        )
        return urljoin(self.base_url, full_url)

    def _make_request(self, request_url: str) -> requests.Response:
        """Make a request to hunters."""
        response = requests.get(request_url, timeout=self.timeout)
        if response.status_code != self.http_ok:
            response.raise_for_status()
        return response
