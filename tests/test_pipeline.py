"""
Comprehensive unit and integration test suite for the Automated Micro-Influencer Outreach System.
"""

import unittest
from src.utils.parsers import parse_follower_count, classify_follower_tier, calculate_engagement_rate
from src.filtering.criteria import FilterCriteria
from src.filtering.classifier import InfluencerClassifier
from src.models.influencer import DiscoveredInfluencer, PlatformMetric
from src.models.enrichment import EnrichedInfluencer
from src.personalization.generator import PersonalizationEngine
from src.sending.validator import OutreachValidator
from src.sending.dispatcher import EmailDispatcher


class TestInfluencerPipeline(unittest.TestCase):

    def test_parse_follower_count(self):
        """Tests parsing of various follower string formats."""
        self.assertEqual(parse_follower_count("60.2k"), 60200)
        self.assertEqual(parse_follower_count("480.4k Followers"), 480400)
        self.assertEqual(parse_follower_count("1.2M"), 1200000)
        self.assertEqual(parse_follower_count("500"), 500)
        self.assertEqual(parse_follower_count("10k-25k Followers"), 17500)
        self.assertEqual(parse_follower_count(""), 0)

    def test_classify_follower_tier(self):
        """Tests categorization into Nano, Micro, and Macro."""
        self.assertEqual(classify_follower_tier(500), "Nano (<5k)")
        self.assertEqual(classify_follower_tier(5000), "Micro (5k-100k)")
        self.assertEqual(classify_follower_tier(56800), "Micro (5k-100k)")
        self.assertEqual(classify_follower_tier(100000), "Micro (5k-100k)")
        self.assertEqual(classify_follower_tier(100001), "Macro (>100k)")

    def test_filtering_and_classification(self):
        """Tests quantitative and qualitative rules evaluation."""
        criteria = FilterCriteria(min_followers=5000, max_followers=100000, min_engagement_rate=2.0)
        classifier = InfluencerClassifier(criteria)

        # 1. Valid micro-influencer (should pass)
        valid_creator = DiscoveredInfluencer(
            id="TEST-001",
            name="Valid Tech Creator",
            username="validtech",
            primary_platform="Instagram",
            profile_url="https://example.com/valid",
            follower_count=35000,
            follower_tier="Micro (5k-100k)",
            estimated_engagement_rate=3.2,
            category="Technology & AI",
            content_themes=["AI & LLMs", "SaaS & Cloud"],
            location="San Francisco, US",
            headline="AI Engineer & Content Creator",
            bio="Building generative AI agents and SaaS tools.",
            platforms=[PlatformMetric(platform="Instagram", follower_count=35000)],
            discovery_source="Test"
        )
        res_valid = classifier.classify(valid_creator)
        self.assertEqual(res_valid.classification.status, "PASSED")
        self.assertGreaterEqual(res_valid.classification.brand_fit_score, 7.0)

        # 2. Too small (<5k Nano - should fail)
        nano_creator = valid_creator.model_copy(update={"follower_count": 800, "follower_tier": "Nano (<5k)"})
        res_nano = classifier.classify(nano_creator)
        self.assertEqual(res_nano.classification.status, "FAILED")
        self.assertTrue(any("below the micro-influencer threshold" in r for r in res_nano.classification.detailed_reasons))

        # 3. Too large (>100k Macro - should fail)
        macro_creator = valid_creator.model_copy(update={"follower_count": 250000, "follower_tier": "Macro (>100k)"})
        res_macro = classifier.classify(macro_creator)
        self.assertEqual(res_macro.classification.status, "FAILED")
        self.assertTrue(any("exceeds the micro-influencer ceiling" in r for r in res_macro.classification.detailed_reasons))

        # 4. Low engagement (<2.0% - should fail)
        low_er_creator = valid_creator.model_copy(update={"estimated_engagement_rate": 1.2})
        res_er = classifier.classify(low_er_creator)
        self.assertEqual(res_er.classification.status, "FAILED")
        self.assertTrue(any("below minimum threshold" in r for r in res_er.classification.detailed_reasons))

    def test_personalization_word_counts(self):
        """Verifies strict adherence to 60-90 words for email and 15-30 words for DM."""
        engine = PersonalizationEngine()
        dummy_enriched = EnrichedInfluencer(
            id="TEST-002",
            name="Alex Rivera",
            platform="TikTok",
            profile_url="https://example.com/alex",
            follower_count=42000,
            engagement_rate=3.1,
            category_niche="Technology & AI",
            content_themes=["AI & LLMs", "Productivity"],
            contact_email="alex@rivera.tech",
            audience_geography="Austin, TX, US",
            content_tone_style="Practical, hands-on, educational",
            recent_content_topics=["Generative AI Workflows"],
            headline="Tech UGC Creator",
            bio="Reviewing AI tools and SaaS apps."
        )

        msg = engine.generate(dummy_enriched)

        # Email word count check: 60 - 90 words
        self.assertGreaterEqual(msg.email_word_count, 60, f"Email word count {msg.email_word_count} < 60")
        self.assertLessEqual(msg.email_word_count, 90, f"Email word count {msg.email_word_count} > 90")
        self.assertTrue(msg.is_email_valid_length)

        # Instagram DM word count check: 15 - 30 words
        self.assertGreaterEqual(msg.dm_word_count, 15, f"DM word count {msg.dm_word_count} < 15")
        self.assertLessEqual(msg.dm_word_count, 30, f"DM word count {msg.dm_word_count} > 30")
        self.assertTrue(msg.is_dm_valid_length)

    def test_validator_and_duplicate_prevention(self):
        """Tests email validation and duplicate outreach rejection."""
        validator = OutreachValidator()

        # Valid email
        is_ok, reason = validator.validate("test@example.com")
        self.assertTrue(is_ok)
        self.assertEqual(reason, "VALID")

        # Register sent
        validator.register_sent("test@example.com")

        # Attempt duplicate outreach to same address
        is_dup, dup_reason = validator.validate("test@example.com")
        self.assertFalse(is_dup)
        self.assertIn("SKIPPED_DUPLICATE", dup_reason)

        # Missing email ('Not Found')
        is_nf, nf_reason = validator.validate("Not Found")
        self.assertFalse(is_nf)
        self.assertIn("SKIPPED_NO_EMAIL", nf_reason)

    def test_simulation_dispatcher(self):
        """Verifies simulated dispatch produces synthetic message IDs and timestamps."""
        dispatcher = EmailDispatcher(mode="simulation")
        res = dispatcher.dispatch(
            recipient_email="creator@test.com",
            subject="Test Subject",
            body="Hello, this is a test collaboration email."
        )
        self.assertTrue(res.success)
        self.assertEqual(res.status, "SIMULATED_SENT")
        self.assertIn("msg_sim_", res.message_id)


if __name__ == "__main__":
    unittest.main()
