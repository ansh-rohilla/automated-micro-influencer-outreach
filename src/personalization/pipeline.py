"""
Pipeline orchestrator for Step 4: AI Message Personalization.
"""

import os
import json
import logging
import pandas as pd
from typing import List, Optional

from src.models.enrichment import EnrichedInfluencer
from src.models.personalization import PersonalizedMessage, PersonalizationBatch
from src.personalization.generator import PersonalizationEngine

logger = logging.getLogger(__name__)


class PersonalizationPipeline:
    """
    Coordinates AI personalized outreach generation across all shortlisted micro-influencers,
    validating word count requirements and persisting datasets.
    """

    def __init__(
        self,
        input_file: str = "data/processed/enriched_influencers.json",
        output_dir: str = "data/processed"
    ):
        self.input_file = input_file
        self.output_dir = output_dir
        self.engine = PersonalizationEngine()
        os.makedirs(self.output_dir, exist_ok=True)

    def run(
        self,
        enriched_list: Optional[List[EnrichedInfluencer]] = None
    ) -> PersonalizationBatch:
        """Executes message personalization generation for all shortlisted creators."""
        if enriched_list is None:
            enriched_list = self._load_enriched_influencers()

        logger.info(f"Generating personalized outreach for {len(enriched_list)} shortlisted creators...")
        messages: List[PersonalizedMessage] = []

        total_email_words = 0
        total_dm_words = 0

        for inf in enriched_list:
            msg = self.engine.generate(inf)
            messages.append(msg)
            total_email_words += msg.email_word_count
            total_dm_words += msg.dm_word_count

        n = len(messages)
        batch = PersonalizationBatch(
            records=messages,
            total_generated=n,
            average_email_words=round(total_email_words / n, 1) if n > 0 else 0.0,
            average_dm_words=round(total_dm_words / n, 1) if n > 0 else 0.0
        )

        logger.info(
            f"Personalization complete. Generated {n} pitches. "
            f"Avg Email words: {batch.average_email_words} (Target: 60-90) | "
            f"Avg DM words: {batch.average_dm_words} (Target: 15-30)"
        )

        self._save_results(batch)
        return batch

    def _load_enriched_influencers(self) -> List[EnrichedInfluencer]:
        """Loads enriched influencer profiles from disk."""
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(
                f"Enriched profile data not found at {self.input_file}. Please run enrichment first."
            )
        with open(self.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [EnrichedInfluencer(**item) for item in data]

    def _save_results(self, batch: PersonalizationBatch):
        """Saves generated messages to CSV and JSON formats."""
        json_path = os.path.join(self.output_dir, "personalized_outreach.json")
        csv_path = os.path.join(self.output_dir, "personalized_outreach.csv")

        # Save JSON
        data_dicts = [item.model_dump() for item in batch.records]
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_dicts, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved personalized outreach JSON to {json_path}")

        # Flatten for CSV representation
        flat_rows = []
        for msg in batch.records:
            flat_rows.append({
                "Influencer_ID": msg.influencer_id,
                "Influencer_Name": msg.influencer_name,
                "Platform": msg.platform,
                "Contact_Email": msg.contact_email,
                "Collaboration_Angle": msg.collaboration_angle,
                "Email_Subject": msg.email_subject,
                "Email_Pitch": msg.email_pitch,
                "Email_Word_Count": msg.email_word_count,
                "Email_Valid_Length (60-90)": "YES" if msg.is_email_valid_length else "NO",
                "Instagram_DM": msg.instagram_dm,
                "DM_Word_Count": msg.dm_word_count,
                "DM_Valid_Length (15-30)": "YES" if msg.is_dm_valid_length else "NO",
                "Value_Proposition": msg.value_proposition
            })

        df = pd.DataFrame(flat_rows)
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved personalized outreach CSV ({len(df)} rows) to {csv_path}")
