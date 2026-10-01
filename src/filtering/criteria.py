"""
Filtering and classification criteria configuration.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class FilterCriteria(BaseModel):
    """Configuration criteria for micro-influencer brand qualification."""
    
    # Quantitative thresholds (Micro-influencer standard definition)
    min_followers: int = Field(default=5_000, description="Minimum follower count (5k)")
    max_followers: int = Field(default=100_000, description="Maximum follower count (100k)")
    min_engagement_rate: float = Field(default=2.0, description="Minimum engagement rate percentage (2.0%)")

    # Qualitative brand-fit rules
    target_niches: List[str] = Field(
        default=[
            "technology", "ai", "artificial intelligence", "saas", "software",
            "developer", "coding", "programming", "cybersecurity", "tech",
            "hardware", "fintech", "web3", "machine learning", "cloud"
        ],
        description="Accepted niche and domain keywords"
    )

    excluded_keywords: List[str] = Field(
        default=["gambling", "casino", "nsfw", "adult", "fake", "scam"],
        description="Disqualifying keywords"
    )

    allowed_platforms: List[str] = Field(
        default=["Instagram", "TikTok", "YouTube", "X (Twitter)", "Twitch"],
        description="Supported social platforms"
    )
