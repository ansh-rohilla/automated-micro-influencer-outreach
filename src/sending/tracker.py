"""
Outreach Tracker: Maintains persistent logs of all outreach communications.
"""

import os
import json
import logging
import pandas as pd
from typing import List, Dict, Set
from src.models.outreach import OutreachLogEntry

logger = logging.getLogger(__name__)


class OutreachTracker:
    """
    Tracks and audits all influencer communications, recording delivery status,
    timestamps, message text, and preventing duplicates.
    """

    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = output_dir
        self.csv_path = os.path.join(output_dir, "outreach_tracker.csv")
        self.json_path = os.path.join(output_dir, "outreach_tracker.json")
        self.entries: List[OutreachLogEntry] = []
        self._contacted_emails: Set[str] = set()
        os.makedirs(self.output_dir, exist_ok=True)
        self._load_existing()

    def _load_existing(self):
        """Loads previous logs from disk if available."""
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.entries = [OutreachLogEntry(**item) for item in data]
                for e in self.entries:
                    if e.status in ["SENT", "SIMULATED_SENT"] and "@" in e.email:
                        self._contacted_emails.add(e.email.lower().strip())
                logger.info(f"Loaded {len(self.entries)} existing outreach log records.")
            except Exception as e:
                logger.warning(f"Could not load previous tracker logs: {e}")

    def is_already_contacted(self, email: str) -> bool:
        """Checks if recipient email has already received outreach."""
        if not email or "@" not in email:
            return False
        return email.lower().strip() in self._contacted_emails

    def log(self, entry: OutreachLogEntry):
        """Adds a log entry and marks email as contacted if successful."""
        self.entries.append(entry)
        if entry.status in ["SENT", "SIMULATED_SENT"] and "@" in entry.email:
            self._contacted_emails.add(entry.email.lower().strip())

    def save(self):
        """Persists tracker entries to CSV and JSON formats."""
        # Save JSON
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump([e.model_dump() for e in self.entries], f, indent=2, ensure_ascii=False)
        logger.info(f"Saved outreach tracker JSON to {self.json_path}")

        # Flatten for CSV as requested in Section 7.D
        rows = []
        for e in self.entries:
            rows.append({
                "Log_ID": e.log_id,
                "Influencer": e.influencer,
                "Email": e.email,
                "Channel": e.channel,
                "Platform": e.platform,
                "Collaboration_Angle": e.collaboration_angle,
                "Message_Generated": e.message_generated,
                "Sent_Date": e.sent_date,
                "Status": e.status,
                "Delivery_Mode": e.delivery_mode,
                "Details": e.details
            })

        df = pd.DataFrame(rows)
        df.to_csv(self.csv_path, index=False)
        logger.info(f"Saved outreach tracker CSV ({len(df)} rows) to {self.csv_path}")
