"""Main module."""
from email_verification.client import EmailVerificationClient
from email_verification.database import ResultDatabase


class EmailVerificationService:
    """Email verification service."""
    def __init__(self, api_key: str, db: ResultDatabase):
        """Initialize the service."""
        self.client = EmailVerificationClient(api_key)
        self.db = db

    def perform_verification(self, email: str) -> None:
        """Perform verification."""
        verification_result = self.client.verify_email(email)
        self.db.create_result(verification_result['email'], verification_result['verification_result'])
        print(f'Verification result for {email}: {verification_result["verification_result"]}')

    def show_all_results(self) -> None:
        """Show all results."""
        results = self.db.get_results()
        print('All results in the database:')
        for result in results:
            print(result)
