"""
Pydantic data models for Step 4: AI Message Personalization.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class PersonalizedMessage(BaseModel):
    """Container for individual email pitch and Instagram DM."""
    email_subject: str
    email_pitch: str
    email_word_count: int
    instagram_dm: str
    dm_word_count: int
    collaboration_angle: str
    value_proposition: str
    influencer_id: str
    influencer_name: str
    contact_email: str
    platform: str
    is_email_valid_length: bool = True  # 60 - 90 words
    is_dm_valid_length: bool = True     # 15 - 30 words


class PersonalizationBatch(BaseModel):
    """Collection of generated personalized outreach messages."""
    records: List[PersonalizedMessage] = Field(default_factory=list)
    total_generated: int = 0
    average_email_words: float = 0.0
    average_dm_words: float = 0.0
