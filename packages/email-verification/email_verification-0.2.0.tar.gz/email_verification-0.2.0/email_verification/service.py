"""Main module."""

from email_verification.client import EmailVerificationClient
from email_verification.database import ResultDatabase


class EmailVerificationService(object):
    """Email verification service."""

    def __init__(self, api_key: str, db: ResultDatabase):
        """Initialize the service."""
        self.client = EmailVerificationClient(api_key)
        self.db = db

    def perform_verification(self, email: str) -> tuple[str, str | bool]:
        """Perform verification."""
        verification_result = self.client.verify_email(email)
        self.db.create_result(verification_result['email'], verification_result['verification_result'])
        return email, verification_result['verification_result']

    def get_all_results(self) -> list[dict[str, str | bool]]:
        """Show all results."""
        return self.db.get_results()
