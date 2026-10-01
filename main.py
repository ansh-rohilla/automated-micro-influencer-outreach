#!/usr/bin/env python3
"""
Master End-to-End Pipeline Orchestrator:
Runs Discovery -> Filtering -> Enrichment -> AI Personalization -> Sending -> Outreach Tracking.
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.discovery.pipeline import DiscoveryPipeline
from src.filtering.pipeline import FilteringPipeline
from src.filtering.criteria import FilterCriteria
from src.enrichment.pipeline import EnrichmentPipeline
from src.personalization.pipeline import PersonalizationPipeline
from src.sending.pipeline import SendingPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MasterPipeline")


def run_full_pipeline(
    niche: str = "Technology & AI",
    target_discovery: int = 50,
    min_followers: int = 5_000,
    max_followers: int = 100_000,
    min_er: float = 2.0,
    sending_mode: str = "simulation"
):
    start_time = datetime.now()
    print("\n" + "=" * 80)
    print("      AUTOMATED MICRO-INFLUENCER OUTREACH SYSTEM")
    print("      End-to-End Pipeline Execution")
    print("=" * 80)
    print(f"Target Niche:             {niche}")
    print(f"Target Discovery Count:   {target_discovery}+ profiles")
    print(f"Follower Bounds:          {min_followers:,} – {max_followers:,}")
    print(f"Min Engagement Rate:      {min_er}%")
    print(f"Sending Layer Mode:       {sending_mode.upper()}")
    print("=" * 80 + "\n")

    # Phase 1: Discovery
    print(">>> [1/5] Executing Influencer Discovery...")
    discovery_pipe = DiscoveryPipeline(output_dir="data/raw")
    discovered = discovery_pipe.run(niche=niche, target_count=target_discovery)
    print(f"    [✓] Discovered {len(discovered)} creators.\n")

    # Phase 2: Filtering & Classification
    print(">>> [2/5] Executing Filtering & Classification Engine...")
    criteria = FilterCriteria(
        min_followers=min_followers,
        max_followers=max_followers,
        min_engagement_rate=min_er
    )
    filtering_pipe = FilteringPipeline(criteria=criteria)
    all_classified, shortlisted = filtering_pipe.run(discovered)
    print(f"    [✓] Evaluated: {len(all_classified)} | Shortlisted (Passed): {len(shortlisted)} | Excluded: {len(all_classified) - len(shortlisted)}\n")

    # Phase 3: Profile Enrichment
    print(">>> [3/5] Executing Profile Enrichment...")
    enrichment_pipe = EnrichmentPipeline()
    enriched = enrichment_pipe.run(shortlisted)
    print(f"    [✓] Enriched {len(enriched)} micro-influencers with contact, demographics, & context.\n")

    # Phase 4: AI Message Personalization
    print(">>> [4/5] Executing AI Message Personalization Engine...")
    personalization_pipe = PersonalizationPipeline()
    batch = personalization_pipe.run(enriched)
    print(f"    [✓] Generated {batch.total_generated} personalized pitches.")
    print(f"        • Avg Email length: {batch.average_email_words} words (Target: 60-90)")
    print(f"        • Avg DM length:    {batch.average_dm_words} words (Target: 15-30)\n")

    # Phase 5: Sending Layer & Outreach Tracking
    print(">>> [5/5] Executing Sending Layer & Duplicate Prevention...")
    sending_pipe = SendingPipeline(mode=sending_mode)
    stats = sending_pipe.run(batch.records, include_instagram_dms=True)
    print(f"    [✓] Dispatch Complete:")
    print(f"        • Emails Delivered/Simulated: {stats['email_sent_or_simulated']}")
    print(f"        • Skipped (No email):          {stats['skipped_no_email']}")
    print(f"        • Skipped (Duplicates):        {stats['skipped_duplicate']}")
    print(f"        • Instagram DMs Processed:     {stats['instagram_dms_processed']}\n")

    elapsed = (datetime.now() - start_time).total_seconds()
    print("=" * 80)
    print(f"  END-TO-END PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f}s")
    print("=" * 80)
    print("Output Datasets Generated:")
    print("  1. Discovered Influencers:      data/raw/discovered_influencers.csv")
    print("  2. Full Classification Audit:   data/processed/classified_influencers.csv")
    print("  3. Shortlisted Influencers:     data/processed/shortlisted_influencers.csv")
    print("  4. Enriched Profiles:           data/processed/enriched_influencers.csv")
    print("  5. Personalized Messages:       data/processed/personalized_outreach.csv")
    print("  6. Live Outreach Tracker:       data/processed/outreach_tracker.csv")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master Influencer Outreach Pipeline")
    parser.add_argument("--niche", default="Technology & AI", help="Target niche")
    parser.add_argument("--count", type=int, default=50, help="Minimum discovery count")
    parser.add_argument("--mode", default="simulation", choices=["simulation", "smtp"], help="Sending mode")
    args = parser.parse_args()

    run_full_pipeline(
        niche=args.niche,
        target_discovery=args.count,
        sending_mode=args.mode
    )
