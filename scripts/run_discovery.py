#!/usr/bin/env python3
"""
Step 1 Discovery Runner: Fetches at least 50 real Tech & AI micro-influencers.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from src.discovery.pipeline import DiscoveryPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("DiscoveryRunner")


def main():
    print("=" * 70)
    print("  AUTOMATED MICRO-INFLUENCER OUTREACH SYSTEM")
    print("  Step 1: Influencer Discovery (Technology & AI Niche)")
    print("=" * 70)

    pipeline = DiscoveryPipeline(output_dir="data/raw")
    discovered = pipeline.run(niche="Technology & AI", target_count=50)

    print("\n" + "=" * 70)
    print(f"  DISCOVERY COMPLETE: {len(discovered)} CREATORS RETRIEVED")
    print("=" * 70)

    # Calculate statistics
    tiers = {}
    platforms = {}
    for inf in discovered:
        tiers[inf.follower_tier] = tiers.get(inf.follower_tier, 0) + 1
        platforms[inf.primary_platform] = platforms.get(inf.primary_platform, 0) + 1

    print("\n[+] Breakdown by Audience Tier:")
    for tier, count in sorted(tiers.items()):
        print(f"    - {tier}: {count}")

    print("\n[+] Breakdown by Primary Platform:")
    for plat, count in sorted(platforms.items()):
        print(f"    - {plat}: {count}")

    print("\n[+] Sample Discovered Influencers:")
    for inf in discovered[:5]:
        print(f"    • {inf.name} (@{inf.username}) | {inf.primary_platform} | {inf.follower_count:,} followers | ER: {inf.estimated_engagement_rate}% | Loc: {inf.location}")
        print(f"      Themes: {', '.join(inf.content_themes)}")
        print(f"      URL: {inf.profile_url}")
        print()

    print(f"[✓] Saved raw dataset to:")
    print(f"    - data/raw/discovered_influencers.json")
    print(f"    - data/raw/discovered_influencers.csv")
    print("=" * 70)


if __name__ == "__main__":
    main()
