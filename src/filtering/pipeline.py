"""
Pipeline orchestrator for Filtering & Classification.
"""

import os
import json
import logging
import pandas as pd
from typing import List, Optional, Tuple

from src.filtering.criteria import FilterCriteria
from src.filtering.classifier import InfluencerClassifier
from src.models.influencer import DiscoveredInfluencer, ClassifiedInfluencer

logger = logging.getLogger(__name__)


class FilteringPipeline:
    """
    Coordinates filtering and classification across discovered influencers,
    saving structured audit reports and candidate shortlists.
    """

    def __init__(
        self,
        criteria: Optional[FilterCriteria] = None,
        input_file: str = "data/raw/discovered_influencers.json",
        output_dir: str = "data/processed"
    ):
        self.criteria = criteria or FilterCriteria()
        self.classifier = InfluencerClassifier(self.criteria)
        self.input_file = input_file
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run(
        self,
        influencers: Optional[List[DiscoveredInfluencer]] = None
    ) -> Tuple[List[ClassifiedInfluencer], List[ClassifiedInfluencer]]:
        """
        Executes the filtering and classification process.

        Returns:
            Tuple of (all_classified, shortlisted_qualified)
        """
        if influencers is None:
            influencers = self._load_discovered_influencers()

        logger.info(f"Initiating filtering on {len(influencers)} discovered profiles...")
        classified_list: List[ClassifiedInfluencer] = []
        shortlisted: List[ClassifiedInfluencer] = []
        rejected: List[ClassifiedInfluencer] = []

        for inf in influencers:
            res = self.classifier.classify(inf)
            classified_list.append(res)
            if res.classification.status == "PASSED":
                shortlisted.append(res)
            else:
                rejected.append(res)

        logger.info(
            f"Filtering complete. Total evaluated: {len(classified_list)} | "
            f"PASSED (Shortlisted): {len(shortlisted)} | FAILED: {len(rejected)}"
        )

        self._save_results(classified_list, shortlisted)
        return classified_list, shortlisted

    def _load_discovered_influencers(self) -> List[DiscoveredInfluencer]:
        """Load discovered influencers from raw data directory."""
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(
                f"Raw discovery data not found at {self.input_file}. Please run discovery first."
            )
        with open(self.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [DiscoveredInfluencer(**item) for item in data]

    def _save_results(
        self,
        all_classified: List[ClassifiedInfluencer],
        shortlisted: List[ClassifiedInfluencer]
    ):
        """Save classified audit dataset and shortlisted candidates."""
        json_path = os.path.join(self.output_dir, "classified_influencers.json")
        csv_path = os.path.join(self.output_dir, "classified_influencers.csv")
        shortlist_csv_path = os.path.join(self.output_dir, "shortlisted_influencers.csv")

        # Save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([item.model_dump() for item in all_classified], f, indent=2, ensure_ascii=False)
        logger.info(f"Saved full classification JSON to {json_path}")

        # Flatten full classification audit CSV
        full_rows = []
        for item in all_classified:
            inf = item.influencer
            cls = item.classification
            full_rows.append({
                "ID": inf.id,
                "Name": inf.name,
                "Username": inf.username,
                "Platform": inf.primary_platform,
                "Followers": inf.follower_count,
                "Follower_Tier": inf.follower_tier,
                "Engagement_Rate": f"{inf.estimated_engagement_rate}%",
                "Niche": inf.category,
                "Status": cls.status,
                "Brand_Fit_Score": f"{cls.brand_fit_score}/10",
                "Primary_Reason": cls.primary_reason,
                "Profile_URL": inf.profile_url,
                "Location": inf.location
            })

        df_all = pd.DataFrame(full_rows)
        df_all.to_csv(csv_path, index=False)
        logger.info(f"Saved classification audit CSV ({len(df_all)} rows) to {csv_path}")

        # Save shortlisted CSV
        shortlist_rows = [row for row in full_rows if row["Status"] == "PASSED"]
        df_shortlist = pd.DataFrame(shortlist_rows)
        df_shortlist.to_csv(shortlist_csv_path, index=False)
        logger.info(f"Saved shortlisted micro-influencers CSV ({len(df_shortlist)} rows) to {shortlist_csv_path}")
