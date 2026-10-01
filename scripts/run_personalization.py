#!/usr/bin/env python3
"""
AI Personalization Runner: Generates bespoke 60-90 word emails and 15-30 word DMs.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from src.personalization.pipeline import PersonalizationPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("PersonalizationRunner")


def main():
    print("=" * 80)
    print("  AUTOMATED MICRO-INFLUENCER OUTREACH SYSTEM")
    print("  AI Personalization Engine (Email Pitch: 60-90w | Instagram DM: 15-30w)")
    print("=" * 80)

    pipeline = PersonalizationPipeline()
    batch = pipeline.run()

    print("\n" + "=" * 80)
    print(f"  PERSONALIZATION SUMMARY: {batch.total_generated} CREATORS PROCESSED")
    print(f"  • Average Email Length: {batch.average_email_words} words (Target: 60 - 90 words)")
    print(f"  • Average Instagram DM Length: {batch.average_dm_words} words (Target: 15 - 30 words)")
    print("=" * 80)

    print("\n[+] Sample Generated Outreach Pairs:\n")
    for msg in batch.records[:3]:
        print(f"┌{'─' * 78}┐")
        print(f"│ CREATOR: {msg.influencer_name} | {msg.platform} | Angle: {msg.collaboration_angle}")
        print(f"│ Contact: {msg.contact_email}")
        print(f"├{'─' * 78}┤")
        print(f"│ [EMAIL PITCH] ({msg.email_word_count} words | Valid 60-90: {msg.is_email_valid_length})")
        print(f"│ Subject: {msg.email_subject}")
        print(f"│ {msg.email_pitch}")
        print(f"├{'─' * 78}┤")
        print(f"│ [INSTAGRAM DM] ({msg.dm_word_count} words | Valid 15-30: {msg.is_dm_valid_length})")
        print(f"│ \"{msg.instagram_dm}\"")
        print(f"└{'─' * 78}┘\n")

    print("[✓] Saved outputs to:")
    print("    - data/processed/personalized_outreach.csv")
    print("    - data/processed/personalized_outreach.json")
    print("=" * 80)


if __name__ == "__main__":
    main()
