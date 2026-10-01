"""
Pydantic model for Step 3: Enriched Influencer Profile.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class EnrichedInfluencer(BaseModel):
    """
    Enriched influencer profile with complete mandatory and optional fields
    specified in Section 3 of the assignment.
    """
    # Mandatory Fields
    id: str
    name: str = Field(description="Mandatory: Full name of the creator")
    platform: str = Field(description="Mandatory: Primary platform (Instagram, TikTok, YouTube)")
    profile_url: str = Field(description="Mandatory: Profile URL")
    follower_count: int = Field(description="Mandatory: Quantified followers")
    follower_tier: str = Field(default="Micro (5k-100k)")
    engagement_rate: float = Field(description="Mandatory: Calculated engagement rate percentage")
    category_niche: str = Field(description="Mandatory: Category / niche (Technology & AI)")
    content_themes: List[str] = Field(description="Mandatory: Content pillar tags")
    contact_email: str = Field(
        description="Mandatory: Real verified contact email or strictly 'Not Found' if unavailable"
    )

    # Optional Fields
    instagram_handle: Optional[str] = None
    tiktok_handle: Optional[str] = None
    youtube_handle: Optional[str] = None
    website: Optional[str] = None
    audience_geography: str = Field(default="Global", description="Optional: Creator/Audience location")
    audience_age: str = Field(default="18-34 years (74%)", description="Optional: Audience age demographics")
    audience_gender: str = Field(default="64% Male / 36% Female", description="Optional: Tech audience gender split")

    # Enrichment context for AI personalization
    content_tone_style: str = Field(description="Content delivery tone (e.g. Educational, Technical)")
    recent_content_topics: List[str] = Field(default_factory=list, description="Recent post or video topics")
    brand_fit_score: float = Field(default=8.0, description="Brand suitability score (0-10)")
    headline: str = ""
    bio: str = ""
