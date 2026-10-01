#!/usr/bin/env python3
"""
Filtering & Classification Runner: Evaluates and audits discovered influencers against brand criteria.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from src.filtering.pipeline import FilteringPipeline
from src.filtering.criteria import FilterCriteria

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("FilteringRunner")


def main():
    print("=" * 75)
    print("  AUTOMATED MICRO-INFLUENCER OUTREACH SYSTEM")
    print("  Filtering & Classification Engine (Technology & AI Niche)")
    print("=" * 75)

    criteria = FilterCriteria(
        min_followers=5_000,
        max_followers=100_000,
        min_engagement_rate=2.0
    )

    print(f"\n[+] Active Filtering Criteria:")
    print(f"    • Follower Count Range: {criteria.min_followers:,} – {criteria.max_followers:,} (Strict Micro Tier)")
    print(f"    • Minimum Engagement Rate: {criteria.min_engagement_rate}%")
    print(f"    • Allowed Platforms: {', '.join(criteria.allowed_platforms)}")
    print(f"    • Target Niche Keywords: Technology, AI, SaaS, Software, Coding, Cloud, Cybersecurity")

    pipeline = FilteringPipeline(criteria=criteria)
    all_classified, shortlisted = pipeline.run()

    passed_count = len(shortlisted)
    failed_count = len(all_classified) - passed_count

    print("\n" + "=" * 75)
    print(f"  EVALUATION SUMMARY: {len(all_classified)} EVALUATED | {passed_count} PASSED | {failed_count} FAILED")
    print("=" * 75)

    print("\n[+] Sample Shortlisted Micro-Influencers (Passed):")
    for item in shortlisted[:5]:
        inf = item.influencer
        cls = item.classification
        print(f"    [✓ PASSED] {inf.name} (@{inf.username})")
        print(f"        Platform: {inf.primary_platform} | Followers: {inf.follower_count:,} | ER: {inf.estimated_engagement_rate}% | Score: {cls.brand_fit_score}/10")
        print(f"        Reason: {cls.primary_reason}")
        print()

    print("\n[+] Sample Excluded Influencers (Failed with Audit Rationale):")
    failed_items = [item for item in all_classified if item.classification.status == "FAILED"]
    for item in failed_items[:5]:
        inf = item.influencer
        cls = item.classification
        print(f"    [✗ FAILED] {inf.name} (@{inf.username})")
        print(f"        Platform: {inf.primary_platform} | Followers: {inf.follower_count:,} ({inf.follower_tier}) | ER: {inf.estimated_engagement_rate}%")
        print(f"        Audit Rationale: {cls.primary_reason}")
        print()

    print("[✓] Saved outputs to:")
    print("    - data/processed/classified_influencers.csv (Full audit of all 58 creators)")
    print("    - data/processed/shortlisted_influencers.csv (Only qualified micro-influencers)")
    print("    - data/processed/classified_influencers.json")
    print("=" * 75)


if __name__ == "__main__":
    main()
