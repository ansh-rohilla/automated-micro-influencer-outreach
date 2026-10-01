"""
Pydantic data models for Step 5: Sending Layer and Outreach Tracker.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class OutreachLogEntry(BaseModel):
    """Schema for individual outreach attempt logged in the tracker."""
    log_id: str
    influencer_id: str
    influencer: str = Field(description="Influencer Name")
    email: str = Field(description="Recipient Email or 'Not Found'")
    platform: str
    channel: str = Field(default="Email", description="Email or Instagram DM")
    collaboration_angle: str
    message_generated: str = Field(description="Content of sent message")
    sent_date: str = Field(description="ISO timestamp or date")
    status: str = Field(description="SENT | SIMULATED_SENT | SKIPPED_NO_EMAIL | SKIPPED_DUPLICATE | FAILED")
    delivery_mode: str = Field(default="simulation", description="smtp | simulation | manual")
    details: str = Field(default="", description="Diagnostic or error logs")


class DispatchResult(BaseModel):
    """Outcome of attempting to send a single outreach message."""
    success: bool
    status: str
    message_id: Optional[str] = None
    recipient: str
    timestamp: str
    error_message: Optional[str] = None
