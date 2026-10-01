"""
Pipeline orchestrator for Step 3: Profile Enrichment.
"""

import os
import json
import logging
import pandas as pd
from typing import List, Optional

from src.enrichment.enricher import ProfileEnricher
from src.models.influencer import ClassifiedInfluencer
from src.models.enrichment import EnrichedInfluencer

logger = logging.getLogger(__name__)


class EnrichmentPipeline:
    """
    Coordinates profile enrichment for shortlisted micro-influencers,
    populating contact details, demographics, tone, and context signals.
    """

    def __init__(
        self,
        input_file: str = "data/processed/classified_influencers.json",
        output_dir: str = "data/processed"
    ):
        self.input_file = input_file
        self.output_dir = output_dir
        self.enricher = ProfileEnricher()
        os.makedirs(self.output_dir, exist_ok=True)

    def run(
        self,
        classified_items: Optional[List[ClassifiedInfluencer]] = None
    ) -> List[EnrichedInfluencer]:
        """
        Executes profile enrichment workflow on shortlisted micro-influencers.
        """
        if classified_items is None:
            classified_items = self._load_shortlisted_influencers()
        else:
            classified_items = [
                item for item in classified_items
                if item.classification.status == "PASSED"
            ]

        logger.info(f"Initiating enrichment on {len(classified_items)} shortlisted micro-influencers...")
        enriched_list: List[EnrichedInfluencer] = []

        for item in classified_items:
            enriched = self.enricher.enrich(item)
            enriched_list.append(enriched)

        logger.info(f"Enrichment complete. Total enriched records: {len(enriched_list)}")
        self._save_results(enriched_list)
        return enriched_list

    def _load_shortlisted_influencers(self) -> List[ClassifiedInfluencer]:
        """Load classified profiles and filter for PASSED candidates."""
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(
                f"Classified data file not found at {self.input_file}. Please run filtering first."
            )
        with open(self.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_items = [ClassifiedInfluencer(**item) for item in data]
        return [item for item in all_items if item.classification.status == "PASSED"]

    def _save_results(self, enriched: List[EnrichedInfluencer]):
        """Saves enriched records to CSV and JSON formats."""
        json_path = os.path.join(self.output_dir, "enriched_influencers.json")
        csv_path = os.path.join(self.output_dir, "enriched_influencers.csv")

        # Save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([item.model_dump() for item in enriched], f, indent=2, ensure_ascii=False)
        logger.info(f"Saved enriched JSON to {json_path}")

        # Flatten for CSV representation matching Section 3 specification
        flat_rows = []
        for inf in enriched:
            flat_rows.append({
                "ID": inf.id,
                "Influencer_Name": inf.name,
                "Platform": inf.platform,
                "Profile_URL": inf.profile_url,
                "Follower_Count": inf.follower_count,
                "Engagement_Rate": f"{inf.engagement_rate}%",
                "Category_Niche": inf.category_niche,
                "Content_Themes": ", ".join(inf.content_themes),
                "Contact_Email": inf.contact_email,
                "Instagram": inf.instagram_handle or "N/A",
                "TikTok": inf.tiktok_handle or "N/A",
                "YouTube": inf.youtube_handle or "N/A",
                "Website": inf.website or "N/A",
                "Audience_Age": inf.audience_age,
                "Audience_Gender": inf.audience_gender,
                "Audience_Geography": inf.audience_geography,
                "Content_Tone": inf.content_tone_style,
                "Recent_Content_Topics": "; ".join(inf.recent_content_topics),
                "Brand_Fit_Score": f"{inf.brand_fit_score}/10"
            })

        df = pd.DataFrame(flat_rows)
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved enriched CSV dataset ({len(df)} rows) to {csv_path}")
