"""
Pydantic data models for the Influencer Outreach Pipeline.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PlatformMetric(BaseModel):
    """Metrics for an individual social media platform."""
    platform: str
    follower_text: str = ""
    follower_count: int = 0
    profile_url: Optional[str] = None


class RawInfluencer(BaseModel):
    """Raw influencer profile collected from discovery sources."""
    username: str
    name: str
    primary_platform: str = "Instagram"
    profile_url: str
    follower_count: int = 0
    estimated_engagement_rate: float = 0.0  # e.g. 3.2%
    location: str = "Global"
    headline: str = ""
    bio: str = ""
    category: str = "Technology & AI"
    platforms: List[PlatformMetric] = Field(default_factory=list)
    source: str = "Collabstr Marketplace"
    raw_metadata: Dict[str, Any] = Field(default_factory=dict)


class DiscoveredInfluencer(BaseModel):
    """Standardized influencer profile resulting from Step 1 Discovery."""
    id: str
    name: str
    username: str
    primary_platform: str
    profile_url: str
    follower_count: int
    follower_tier: str  # e.g. "Nano (<5k)", "Micro (5k-100k)", "Macro (>100k)"
    estimated_engagement_rate: float
    category: str
    content_themes: List[str] = Field(default_factory=list)
    location: str
    headline: str
    bio: str
    platforms: List[PlatformMetric] = Field(default_factory=list)
    discovery_source: str
