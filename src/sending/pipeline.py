"""
Pipeline orchestrator for Step 5: Sending Layer & Outreach Tracking.
"""

import os
import json
import uuid
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.models.personalization import PersonalizedMessage
from src.models.outreach import OutreachLogEntry
from src.sending.validator import OutreachValidator
from src.sending.dispatcher import EmailDispatcher
from src.sending.instagram_workflow import InstagramDMWorkflow
from src.sending.tracker import OutreachTracker

logger = logging.getLogger(__name__)


class SendingPipeline:
    """
    Coordinates delivery across email and Instagram DM channels:
    1. Selects influencers with valid contact emails.
    2. Validates and prevents duplicate outreach.
    3. Dispatches via SMTP or Simulation mode.
    4. Handles Instagram DM workflow.
    5. Records comprehensive audit log in OutreachTracker.
    """

    def __init__(
        self,
        mode: str = "simulation",
        input_file: str = "data/processed/personalized_outreach.json",
        output_dir: str = "data/processed"
    ):
        self.mode = mode
        self.input_file = input_file
        self.output_dir = output_dir
        self.tracker = OutreachTracker(output_dir)
        self.dispatcher = EmailDispatcher(mode=mode)
        self.validator = OutreachValidator(self.tracker._contacted_emails)
        self.dm_workflow = InstagramDMWorkflow()

    def run(
        self,
        messages: Optional[List[PersonalizedMessage]] = None,
        include_instagram_dms: bool = True
    ) -> Dict[str, Any]:
        """
        Executes sending pipeline across qualified influencers.
        """
        if messages is None:
            messages = self._load_personalized_messages()

        logger.info(f"Initiating SendingPipeline on {len(messages)} messages (mode='{self.mode}')...")

        stats = {
            "total_processed": len(messages),
            "email_sent_or_simulated": 0,
            "skipped_no_email": 0,
            "skipped_duplicate": 0,
            "failed_email": 0,
            "instagram_dms_processed": 0
        }

        # 1. Process Emails
        for msg in messages:
            email = msg.contact_email
            inf_name = msg.influencer_name
            inf_id = msg.influencer_id
            now_str = datetime.now().isoformat()
            log_id = f"LOG-EM-{uuid.uuid4().hex[:8].upper()}"

            # Validate recipient & check duplicate
            is_valid, reason = self.validator.validate(email)

            if not is_valid:
                if "SKIPPED_NO_EMAIL" in reason:
                    stats["skipped_no_email"] += 1
                    status = "SKIPPED_NO_EMAIL"
                elif "SKIPPED_DUPLICATE" in reason:
                    stats["skipped_duplicate"] += 1
                    status = "SKIPPED_DUPLICATE"
                else:
                    stats["failed_email"] += 1
                    status = "FAILED"

                entry = OutreachLogEntry(
                    log_id=log_id,
                    influencer_id=inf_id,
                    influencer=inf_name,
                    email=email,
                    platform=msg.platform,
                    channel="Email",
                    collaboration_angle=msg.collaboration_angle,
                    message_generated=msg.email_pitch,
                    sent_date=now_str,
                    status=status,
                    delivery_mode=self.mode,
                    details=reason
                )
                self.tracker.log(entry)
                continue

            # Dispatch valid email
            dispatch_res = self.dispatcher.dispatch(
                recipient_email=email,
                subject=msg.email_subject,
                body=msg.email_pitch
            )

            if dispatch_res.success:
                stats["email_sent_or_simulated"] += 1
                self.validator.register_sent(email)
                details = f"Delivered successfully. MessageID: {dispatch_res.message_id}"
            else:
                stats["failed_email"] += 1
                details = f"Delivery failed: {dispatch_res.error_message}"

            entry = OutreachLogEntry(
                log_id=log_id,
                influencer_id=inf_id,
                influencer=inf_name,
                email=email,
                platform=msg.platform,
                channel="Email",
                collaboration_angle=msg.collaboration_angle,
                message_generated=msg.email_pitch,
                sent_date=dispatch_res.timestamp,
                status=dispatch_res.status,
                delivery_mode=self.mode,
                details=details
            )
            self.tracker.log(entry)

        # 2. Process Instagram DMs
        if include_instagram_dms:
            for msg in messages:
                dm_entry = self.dm_workflow.prepare_dm_dispatch(
                    influencer_id=msg.influencer_id,
                    influencer_name=msg.influencer_name,
                    handle=f"@{msg.influencer_id}",
                    dm_text=msg.instagram_dm,
                    angle=msg.collaboration_angle,
                    simulated=True
                )
                self.tracker.log(dm_entry)
                stats["instagram_dms_processed"] += 1

        self.tracker.save()
        logger.info(f"Sending pipeline completed. Stats: {stats}")
        return stats

    def _load_personalized_messages(self) -> List[PersonalizedMessage]:
        """Loads personalized outreach records from disk."""
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(
                f"Personalized outreach data not found at {self.input_file}. Please run personalization first."
            )
        with open(self.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [PersonalizedMessage(**item) for item in data]
