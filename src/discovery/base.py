"""
Abstract base class for influencer discovery sources.
"""

from abc import ABC, abstractmethod
from typing import List
from src.models.influencer import RawInfluencer


class BaseDiscoverySource(ABC):
    """Abstract interface for all discovery adapters (Collabstr, YouTube, Public Directories, etc.)."""

    @abstractmethod
    def discover(self, niche: str = "Technology & AI", target_count: int = 50) -> List[RawInfluencer]:
        """
        Discovers influencer profiles matching the specified niche.

        Args:
            niche: Target domain/niche to discover (e.g. 'Technology & AI').
            target_count: Minimum number of candidate influencers to retrieve.

        Returns:
            List of RawInfluencer objects.
        """
        pass
