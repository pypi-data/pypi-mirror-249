"""Service to use email verification client with database."""
import logging
from typing import Dict, List, Tuple

import requests

from email_verification.client import EmailVerificationClient
from email_verification.database import ResultDatabase
from email_verification.utils.response_normilizer import response_normalizer


class EmailVerificationService(object):
    """Email verification service."""

    def __init__(self, api_key: str, db: ResultDatabase, timeout: int = 2) -> None:
        """Initialize the service."""
        self.client = EmailVerificationClient(api_key, timeout)
        self.db = db
        self.logger = logging.getLogger(__name__)

    def count_emails(self, domain: str, **kwargs: str) -> Dict[str, str]:
        """Count the number of emails in the given domain and handle errors."""
        try:
            return self.client.make_request('email-count', domain=domain, **kwargs)
        except requests.exceptions.RequestException as request_exception:
            self.logger.error(
                'Request error for domain {0}: {1}'.format(domain, request_exception),
            )
            return {
                'Error': 'Request error: {request_exception}'.format(
                    request_exception=str(request_exception),
                ),
            }
        except Exception as exception:
            self.logger.error(
                'Unexpected error for domain {0}: {1}'.format(domain, exception),
            )
            return {
                'Error': 'Unexpected error: {exception}'.format(
                    exception=str(exception),
                ),
            }

    def email_verification(self, email: str) -> Dict[str, str]:
        """Email verification using hunter client and database."""
        try:
            verification_result = self.client.make_request('email-verifier', email=email)
        except requests.exceptions.RequestException as request_exception:
            self.logger.error(
                'Request error for email {0}: {1}'.format(email, request_exception),
            )
            return {
                'Request error': '{request_exception}'.format(
                    request_exception=str(request_exception),
                ),
            }
        except Exception as exception:
            self.logger.error(
                'Unexpected error for email {0}: {1}'.format(email, exception),
            )
            return {
                'Unexpected error': '{exception}'.format(
                    exception=str(exception),
                ),
            }
        verification_result = response_normalizer(verification_result)
        email_to_save = verification_result.pop('meta_params_email')
        self.db.create_result(email_to_save, verification_result)
        return verification_result

    def get_all_results(self) -> List[Dict[str, str]]:
        """Show all verification results."""
        return self.db.get_results()

    def delete_result(self, email: str) -> Tuple[str, Dict[str, str]]:
        """Delete result and handle errors."""
        try:
            self.db.delete_result(email)
        except Exception as exception:
            return email, {
                'error': 'Unexpected error: {exception}'.format(
                    exception=str(exception),
                ),
            }
        return email, {'status': 'deleted'}

    def get_result(self, email: str) -> Dict[str, str]:
        """Get verification email if exists."""
        try:
            get_result = self.db.get_result(email)
        except Exception as exception:
            return {
                'error': 'Unexpected error: {exception}'.format(
                    exception=str(exception),
                ),
            }
        return get_result
