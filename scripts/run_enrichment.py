#!/usr/bin/env python3
"""
Profile Enrichment Runner: Enriches shortlisted micro-influencers with mandatory and optional context.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from src.enrichment.pipeline import EnrichmentPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("EnrichmentRunner")


def main():
    print("=" * 75)
    print("  AUTOMATED MICRO-INFLUENCER OUTREACH SYSTEM")
    print("  Profile Enrichment Engine (Shortlisted Micro-Influencers)")
    print("=" * 75)

    pipeline = EnrichmentPipeline()
    enriched_list = pipeline.run()

    emails_found = sum(1 for e in enriched_list if e.contact_email != "Not Found")
    emails_not_found = len(enriched_list) - emails_found

    print("\n" + "=" * 75)
    print(f"  ENRICHMENT SUMMARY: {len(enriched_list)} PROFILES ENRICHED")
    print("=" * 75)

    print(f"\n[+] Contact Email Coverage:")
    print(f"    • Verified Emails Available: {emails_found} profiles")
    print(f"    • Marked 'Not Found' (Anti-Fabrication): {emails_not_found} profiles")

    print("\n[+] Sample Enriched Profiles:")
    for inf in enriched_list[:5]:
        print(f"    • {inf.name} ({inf.platform} - {inf.follower_count:,} followers)")
        print(f"      Contact Email: {inf.contact_email}")
        print(f"      Profile URL: {inf.profile_url}")
        print(f"      Tone/Style: {inf.content_tone_style}")
        print(f"      Recent Topics: {', '.join(inf.recent_content_topics)}")
        print(f"      Demographics: {inf.audience_age} | {inf.audience_gender} | Loc: {inf.audience_geography}")
        print()

    print("[✓] Saved enriched outputs to:")
    print("    - data/processed/enriched_influencers.csv (Complete mandatory & optional fields)")
    print("    - data/processed/enriched_influencers.json")
    print("=" * 75)


if __name__ == "__main__":
    main()
