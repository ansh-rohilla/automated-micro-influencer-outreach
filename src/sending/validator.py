"""
Email validator and duplicate outreach detector.
"""

import re
from typing import Set, Tuple


class OutreachValidator:
    """
    Validates recipient email addresses and prevents duplicate outreach (idempotency).
    """

    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def __init__(self, existing_outreach_emails: Set[str] = None):
        self.sent_emails: Set[str] = existing_outreach_emails or set()

    def validate(self, email: str) -> Tuple[bool, str]:
        """
        Validates whether an email is deliverable and has not already been contacted.
        """
        if not email or email.strip().lower() in ["not found", "n/a", "none"]:
            return False, "SKIPPED_NO_EMAIL: Influencer has no valid public contact email"

        cleaned = email.strip().lower()
        if not re.match(self.EMAIL_REGEX, cleaned):
            return False, f"FAILED_INVALID_EMAIL: Email '{email}' syntax is invalid"

        if cleaned in self.sent_emails:
            return False, f"SKIPPED_DUPLICATE: Influencer '{cleaned}' already contacted in current or prior campaign"

        return True, "VALID"

    def register_sent(self, email: str):
        """Records email in active deduplication set."""
        if email and email.strip().lower() not in ["not found", "n/a"]:
            self.sent_emails.add(email.strip().lower())
