"""Database for email verification service."""
from typing import Dict, List, Union

EmailVerificationResult = Dict[str, Union[str, bool]]


class ResultDatabase(object):
    """Base class with CRUD operations."""

    def __init__(self):
        """Initialize the database."""
        self.checked_emails: List[EmailVerificationResult] = []

    def create_result(self, email: str, verification_result: Union[str, bool]) -> bool:
        """Create if not exist."""
        if self.exists(email):
            self.update_result(email, verification_result)
            return False
        self.checked_emails.append({'email': email, 'verification_result': verification_result})
        return True

    def get_results(self) -> List[EmailVerificationResult]:
        """Get all results."""
        return self.checked_emails

    def delete_result(self, email: str) -> None:
        """Delete if not exist."""
        self.checked_emails = [inner_email for inner_email in self.checked_emails if inner_email['email'] != email]

    def update_result(self, email: str, verification_result: Union[str, bool]) -> None:
        """Update if not exist."""
        for inner_email in self.checked_emails:
            if inner_email['email'] == email:
                inner_email['verification_result'] = verification_result

    def exists(self, email: str) -> bool:
        """Check if email is."""
        return any(inner_email['email'] == email for inner_email in self.checked_emails)
