"""Database."""
from typing import Dict, List


class ResultDatabase(object):
    """Base class with CRUD operations."""

    def __init__(self) -> None:
        """Initialize the database."""
        self.checked_emails: List[Dict[str, str]] = []

    def create_result(self, email: str, verification_result: Dict[str, str]) -> bool:
        """Create if not exist."""
        if self.exists(email):
            self.update_result(email, verification_result)
            return False
        verification_result['email'] = email.upper()
        self.checked_emails.append(verification_result)
        return True

    def get_results(self) -> List[Dict[str, str]]:
        """Get all results."""
        return self.checked_emails

    def get_result(self, email: str) -> Dict[str, str]:
        """Get result for a specific email."""
        for inner_result in self.checked_emails:
            if inner_result['email'].upper() == email.upper():
                return inner_result
        return {'error': 'Result not found for email: {email}'.format(email=email)}

    def delete_result(self, email: str) -> None:
        """Delete if exists."""
        new_checked_emails = []
        for inner_result in self.checked_emails:
            if inner_result['email'].upper() != email.upper():
                new_checked_emails.append(inner_result)
        self.checked_emails = new_checked_emails

    def update_result(self, email: str, verification_result: Dict[str, str]) -> None:
        """Update if exists."""
        for inner_email in self.checked_emails:
            if inner_email['email'] == email.upper():
                inner_email.update(verification_result)

    def exists(self, email: str) -> bool:
        """Check if email exists."""
        return any(inner_email['email'] == email.upper() for inner_email in self.checked_emails)
