"""
Email Dispatcher: Dispatches outreach via SMTP or high-fidelity simulation mode.
"""

import os
import time
import uuid
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from src.models.outreach import DispatchResult

logger = logging.getLogger(__name__)


class EmailDispatcher:
    """
    Handles delivery of personalized pitches using either live SMTP or
    safe, auditable simulation mode.
    """

    def __init__(self, mode: Optional[str] = None):
        self.mode = mode or os.getenv("SENDING_MODE", "simulation").lower()
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.sender_name = os.getenv("SENDER_NAME", "AI Partnerships Lead")

    def dispatch(
        self,
        recipient_email: str,
        subject: str,
        body: str
    ) -> DispatchResult:
        """Dispatches an email via configured mode."""
        timestamp = datetime.now().isoformat()

        if self.mode == "smtp":
            return self._dispatch_smtp(recipient_email, subject, body, timestamp)
        else:
            return self._dispatch_simulated(recipient_email, subject, body, timestamp)

    def _dispatch_simulated(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        timestamp: str
    ) -> DispatchResult:
        """Simulates full SMTP delivery cycle with synthetic message ID and audit trail."""
        message_id = f"<msg_sim_{uuid.uuid4().hex[:12]}@{recipient_email.split('@')[-1]}>"
        # Simulate standard network latency (100ms)
        time.sleep(0.1)

        logger.info(f"[SIMULATION] Dispatched email to {recipient_email} | ID: {message_id}")
        return DispatchResult(
            success=True,
            status="SIMULATED_SENT",
            message_id=message_id,
            recipient=recipient_email,
            timestamp=timestamp,
            error_message=None
        )

    def _dispatch_smtp(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        timestamp: str
    ) -> DispatchResult:
        """Executes live SMTP dispatch."""
        if not self.smtp_user or not self.smtp_password:
            err = "SMTP credentials missing. Please set SMTP_USER and SMTP_PASSWORD in .env"
            logger.error(err)
            return DispatchResult(
                success=False,
                status="FAILED",
                message_id=None,
                recipient=recipient_email,
                timestamp=timestamp,
                error_message=err
            )

        try:
            msg = MIMEMultipart()
            msg["From"] = f"{self.sender_name} <{self.smtp_user}>"
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            msg_id = f"<smtp_{uuid.uuid4().hex[:12]}@{self.smtp_host}>"
            logger.info(f"[LIVE SMTP] Successfully sent email to {recipient_email}")
            return DispatchResult(
                success=True,
                status="SENT",
                message_id=msg_id,
                recipient=recipient_email,
                timestamp=timestamp,
                error_message=None
            )
        except Exception as e:
            logger.error(f"Failed to send email via SMTP to {recipient_email}: {e}")
            return DispatchResult(
                success=False,
                status="FAILED",
                message_id=None,
                recipient=recipient_email,
                timestamp=timestamp,
                error_message=str(e)
            )
