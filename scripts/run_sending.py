#!/usr/bin/env python3
"""
Sending Layer Runner: Delivers pitches (Email simulation/SMTP + Instagram DM) and maintains Outreach Tracker.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from src.sending.pipeline import SendingPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("SendingRunner")


def main():
    print("=" * 80)
    print("  AUTOMATED MICRO-INFLUENCER OUTREACH SYSTEM")
    print("  Sending Layer & Idempotent Outreach Tracker")
    print("=" * 80)

    mode = os.getenv("SENDING_MODE", "simulation").lower()
    print(f"\n[+] Active Delivery Mode: {mode.upper()}")
    print("    • Selects only influencers with valid contact emails")
    print("    • Prevents duplicate outreach (Idempotent tracking)")
    print("    • Compliant Instagram DM workflow")

    pipeline = SendingPipeline(mode=mode)
    stats = pipeline.run(include_instagram_dms=True)

    print("\n" + "=" * 80)
    print("  OUTREACH DISPATCH SUMMARY:")
    print(f"  • Total Influencers Evaluated: {stats['total_processed']}")
    print(f"  • Emails Sent / Simulated:      {stats['email_sent_or_simulated']}")
    print(f"  • Skipped (No Contact Email):   {stats['skipped_no_email']}")
    print(f"  • Skipped (Duplicate Check):    {stats['skipped_duplicate']}")
    print(f"  • Instagram DMs Processed:      {stats['instagram_dms_processed']}")
    print("=" * 80)

    # Re-run a second time to demonstrate duplicate prevention in action!
    print("\n[+] Testing Idempotency & Duplicate Prevention (Immediate Re-run Check)...")
    re_run_stats = pipeline.run(include_instagram_dms=False)
    print(f"    • Duplicates Successfully Prevented: {re_run_stats['skipped_duplicate']}")

    print("\n[✓] Saved complete outreach audit trail to:")
    print("    - data/processed/outreach_tracker.csv")
    print("    - data/processed/outreach_tracker.json")
    print("=" * 80)


if __name__ == "__main__":
    main()
