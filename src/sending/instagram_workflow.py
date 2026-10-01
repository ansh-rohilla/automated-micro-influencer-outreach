"""
Instagram DM Workflow: Compliant manual/simulated direct message dispatch workflow.
"""

import uuid
import logging
from datetime import datetime
from typing import Dict, Any
from src.models.outreach import OutreachLogEntry

logger = logging.getLogger(__name__)


class InstagramDMWorkflow:
    """
    Manages Instagram DM delivery in compliance with platform terms,
    offering simulated delivery and manual copy-dispatch tracking.
    """

    def prepare_dm_dispatch(
        self,
        influencer_id: str,
        influencer_name: str,
        handle: str,
        dm_text: str,
        angle: str,
        simulated: bool = True
    ) -> OutreachLogEntry:
        """Packages a DM for simulated dispatch or manual copy-workflow."""
        log_id = f"LOG-DM-{uuid.uuid4().hex[:8].upper()}"
        now_str = datetime.now().isoformat()

        status = "SIMULATED_DM_SENT" if simulated else "READY_FOR_MANUAL_DISPATCH"
        details = (
            f"Instagram DM dispatched via simulated workflow to {handle}"
            if simulated else f"Ready for copy-to-clipboard dispatch to {handle}"
        )

        logger.info(f"[INSTAGRAM DM] {status} for {influencer_name} ({handle})")

        return OutreachLogEntry(
            log_id=log_id,
            influencer_id=influencer_id,
            influencer=influencer_name,
            email=handle or "N/A (Instagram DM)",
            platform="Instagram",
            channel="Instagram DM",
            collaboration_angle=angle,
            message_generated=dm_text,
            sent_date=now_str,
            status=status,
            delivery_mode="simulation" if simulated else "manual",
            details=details
        )
