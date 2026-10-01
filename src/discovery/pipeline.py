"""
Pipeline orchestrator for Step 1: Influencer Discovery.
"""

import os
import json
import logging
import pandas as pd
from typing import List, Optional

from src.discovery.base import BaseDiscoverySource
from src.discovery.collabstr import CollabstrDiscoverySource
from src.models.influencer import DiscoveredInfluencer, RawInfluencer
from src.utils.parsers import classify_follower_tier, extract_content_themes

logger = logging.getLogger(__name__)


class DiscoveryPipeline:
    """
    Coordinates multi-source influencer discovery, deduplication,
    standardization, and persistence to disk.
    """

    def __init__(self, sources: Optional[List[BaseDiscoverySource]] = None, output_dir: str = "data/raw"):
        self.sources = sources or [CollabstrDiscoverySource()]
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, niche: str = "Technology & AI", target_count: int = 50) -> List[DiscoveredInfluencer]:
        """
        Executes discovery workflow and ensures at least target_count influencers are returned.
        """
        logger.info(f"Starting DiscoveryPipeline for '{niche}' (min requirement: {target_count})...")
        raw_candidates: List[RawInfluencer] = []

        for source in self.sources:
            try:
                results = source.discover(niche=niche, target_count=target_count)
                raw_candidates.extend(results)
            except Exception as e:
                logger.error(f"Error in discovery source {source.__class__.__name__}: {e}")

        # Deduplicate by username / profile URL
        unique_map = {}
        for r in raw_candidates:
            key = r.username.lower().strip()
            if key not in unique_map:
                unique_map[key] = r

        deduped = list(unique_map.values())
        logger.info(f"Total unique raw influencers found: {len(deduped)}")

        # Convert to standardized DiscoveredInfluencer models
        standardized: List[DiscoveredInfluencer] = []
        for i, raw in enumerate(deduped, start=1):
            tier = classify_follower_tier(raw.follower_count)
            themes = extract_content_themes(raw.bio, raw.headline, default_niche=raw.category)

            item = DiscoveredInfluencer(
                id=f"INF-{i:03d}",
                name=raw.name,
                username=raw.username,
                primary_platform=raw.primary_platform,
                profile_url=raw.profile_url,
                follower_count=raw.follower_count,
                follower_tier=tier,
                estimated_engagement_rate=raw.estimated_engagement_rate,
                category=raw.category,
                content_themes=themes,
                location=raw.location,
                headline=raw.headline,
                bio=raw.bio,
                platforms=raw.platforms,
                discovery_source=raw.source
            )
            standardized.append(item)

        if len(standardized) < target_count:
            logger.warning(
                f"Discovery retrieved {len(standardized)} creators, which is below target {target_count}."
            )
        else:
            logger.info(f"Discovery successfully exceeded target! Retrieved {len(standardized)} creators.")

        self._save_datasets(standardized)
        return standardized

    def _save_datasets(self, influencers: List[DiscoveredInfluencer]):
        """Persist discovered influencer records to CSV and JSON formats."""
        json_path = os.path.join(self.output_dir, "discovered_influencers.json")
        csv_path = os.path.join(self.output_dir, "discovered_influencers.csv")

        # Save JSON
        data_dicts = [inf.model_dump() for inf in influencers]
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_dicts, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved JSON dataset to {json_path}")

        # Flatten for CSV representation matching assignment specification
        flat_records = []
        for inf in influencers:
            flat_records.append({
                "ID": inf.id,
                "Name": inf.name,
                "Username": inf.username,
                "Platform": inf.primary_platform,
                "Followers": inf.follower_count,
                "Follower_Tier": inf.follower_tier,
                "Engagement_Rate": f"{inf.estimated_engagement_rate}%",
                "Niche": inf.category,
                "Content_Themes": ", ".join(inf.content_themes),
                "Location": inf.location,
                "Profile_URL": inf.profile_url,
                "Headline": inf.headline,
                "Bio": inf.bio,
                "Discovery_Source": inf.discovery_source
            })

        df = pd.DataFrame(flat_records)
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved CSV dataset ({len(df)} rows) to {csv_path}")
