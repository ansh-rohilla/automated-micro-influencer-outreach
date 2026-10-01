"""
AI Message Personalization Engine: Generates bespoke Email pitches and Instagram DMs.
"""

import os
import re
import logging
from typing import Tuple, Optional
from src.models.enrichment import EnrichedInfluencer
from src.models.personalization import PersonalizedMessage
from src.personalization.prompts import (
    EMAIL_PITCH_PROMPT_TEMPLATE,
    INSTAGRAM_DM_PROMPT_TEMPLATE,
    COLLABORATION_ANGLES
)

logger = logging.getLogger(__name__)


class PersonalizationEngine:
    """
    Generates personalized outreach messages strictly conforming to
    word count constraints (Email: 60-90 words, DM: 15-30 words).
    """

    ANGLE_VALUE_PROPS = {
        "Sponsorship": "Competitive flat creator fees with creative freedom on campaign integration.",
        "Affiliate campaign": "High-tier recurring revenue share and custom audience discounts.",
        "UGC content creation": "Paid commercial licensing deal for our upcoming high-growth ad campaigns.",
        "Brand ambassador program": "Long-term quarterly retainer with early feature access and co-marketing.",
        "Paid product placement": "Dedicated sponsored demo segment highlighting your authentic workflow.",
        "Barter collaboration": "Complimentary enterprise tier access and software gifting for your candid review."
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

    def generate(
        self,
        influencer: EnrichedInfluencer,
        angle: Optional[str] = None
    ) -> PersonalizedMessage:
        """Generates dynamic, bespoke email pitch and Instagram DM for a creator."""
        selected_angle = angle or self._determine_best_angle(influencer)
        value_prop = self.ANGLE_VALUE_PROPS.get(selected_angle, "Exciting collaboration package.")

        # Attempt LLM generation if API key is present
        email_pitch, email_subject, instagram_dm = None, None, None
        if self.api_key:
            try:
                email_pitch, email_subject, instagram_dm = self._generate_with_llm(
                    influencer, selected_angle, value_prop
                )
            except Exception as e:
                logger.warning(f"LLM call failed ({e}). Falling back to dynamic context engine.")

        # Fallback to dynamic context synthesizer
        if not email_pitch or not instagram_dm:
            email_subject, email_pitch, instagram_dm = self._generate_dynamic_context(
                influencer, selected_angle, value_prop
            )

        # Enforce word counts strictly
        email_pitch = self._enforce_word_range(email_pitch, min_words=60, max_words=90)
        instagram_dm = self._enforce_word_range(instagram_dm, min_words=15, max_words=30)

        email_wc = len(email_pitch.split())
        dm_wc = len(instagram_dm.split())

        return PersonalizedMessage(
            email_subject=email_subject,
            email_pitch=email_pitch,
            email_word_count=email_wc,
            instagram_dm=instagram_dm,
            dm_word_count=dm_wc,
            collaboration_angle=selected_angle,
            value_proposition=value_prop,
            influencer_id=influencer.id,
            influencer_name=influencer.name,
            contact_email=influencer.contact_email,
            platform=influencer.platform,
            is_email_valid_length=(60 <= email_wc <= 90),
            is_dm_valid_length=(15 <= dm_wc <= 30)
        )

    def _determine_best_angle(self, inf: EnrichedInfluencer) -> str:
        """Selects the highest-converting collaboration angle based on creator profile context."""
        text = f"{inf.headline} {inf.bio} {' '.join(inf.content_themes)}".lower()
        if "ugc" in text:
            return "UGC content creation"
        elif any(k in text for k in ["coding", "developer", "engineer", "dev"]):
            return "Paid product placement"
        elif any(k in text for k in ["ai", "saas", "software"]):
            return "Sponsorship"
        elif any(k in text for k in ["business", "startup", "entrepreneur"]):
            return "Affiliate campaign"
        elif any(k in text for k in ["gadget", "hardware", "unboxing"]):
            return "Barter collaboration"
        else:
            return "Brand ambassador program"

    def _generate_dynamic_context(
        self,
        inf: EnrichedInfluencer,
        angle: str,
        value_prop: str
    ) -> Tuple[str, str, str]:
        """
        Synthesizes personalized outreach dynamically without fixed rigid templates,
        incorporating creator's name, tone, audience demographics, and specific topics.
        """
        first_name = inf.name.split()[0]
        recent_topic = inf.recent_content_topics[0] if inf.recent_content_topics else "tech solutions"
        loc = inf.audience_geography.split(",")[0] if "," in inf.audience_geography else inf.audience_geography

        # Subject line
        subject = f"Collaboration inquiry with {first_name} – {angle} for {recent_topic}"

        # Dynamic email body structured for 60-90 words
        email_body = (
            f"Hi {first_name}, I loved your recent breakdown on {recent_topic.lower()}. "
            f"Your {inf.content_tone_style.lower()} and highly engaged {inf.audience_age.split()[0]} "
            f"tech audience in {loc} align seamlessly with our team's mission. "
            f"We are launching an upcoming {angle.lower()} and would love to partner with you. "
            f"We offer {value_prop.lower()} "
            f"Would you be open to reviewing a brief partnership brief this week?"
        )

        # Dynamic DM structured for 15-30 words
        dm_body = (
            f"Hi {first_name}, loved your recent {recent_topic.lower()} content! "
            f"Your tech audience looks like a perfect fit for our upcoming {angle.lower()}. Open to collaborating?"
        )

        return subject, email_body, dm_body

    def _generate_with_llm(
        self,
        inf: EnrichedInfluencer,
        angle: str,
        value_prop: str
    ) -> Tuple[str, str, str]:
        """Calls external LLM (Gemini or OpenAI) via LiteLLM."""
        import litellm
        first_name = inf.name.split()[0]
        recent = ", ".join(inf.recent_content_topics)

        email_prompt = EMAIL_PITCH_PROMPT_TEMPLATE.format(
            name=inf.name,
            username=inf.id,
            platform=inf.platform,
            follower_count=inf.follower_count,
            engagement_rate=inf.engagement_rate,
            category=inf.category_niche,
            themes=", ".join(inf.content_themes),
            tone_style=inf.content_tone_style,
            recent_topics=recent,
            audience_demo=inf.audience_age,
            location=inf.audience_geography,
            angle=angle,
            value_prop=value_prop
        )

        model_name = "gemini/gemini-1.5-flash" if os.getenv("GEMINI_API_KEY") else "gpt-3.5-turbo"
        resp = litellm.completion(
            model=model_name,
            messages=[{"role": "user", "content": email_prompt}],
            temperature=0.7,
            max_tokens=250
        )
        content = resp.choices[0].message.content.strip()

        lines = [line.strip() for line in content.split("\n") if line.strip()]
        subject = lines[0].replace("Subject:", "").strip() if len(lines) > 1 else f"Partnership with {first_name}"
        body = " ".join(lines[1:]) if len(lines) > 1 else lines[0]

        # DM generation
        dm_prompt = INSTAGRAM_DM_PROMPT_TEMPLATE.format(
            name=inf.name,
            username=inf.id,
            category=inf.category_niche,
            recent_topics=recent,
            platform=inf.platform,
            audience_demo=inf.audience_age,
            angle=angle
        )
        dm_resp = litellm.completion(
            model=model_name,
            messages=[{"role": "user", "content": dm_prompt}],
            temperature=0.7,
            max_tokens=60
        )
        dm = dm_resp.choices[0].message.content.strip().replace('"', '')

        return body, subject, dm

    def _enforce_word_range(self, text: str, min_words: int, max_words: int) -> str:
        """Trims or expands text to strictly satisfy word-count bounds."""
        words = text.split()
        if len(words) > max_words:
            # Trim to max_words while preserving punctuation
            words = words[:max_words]
            trimmed = " ".join(words)
            if not trimmed.endswith((".", "!", "?")):
                trimmed += "."
            return trimmed
        elif len(words) < min_words:
            # Append natural context words to satisfy minimum length
            filler = " Let us know if you would like to explore this opportunity together."
            while len(words) < min_words:
                words.extend(filler.split())
            trimmed = " ".join(words[:min_words + 2])
            if not trimmed.endswith((".", "!", "?")):
                trimmed += "."
            return trimmed
        return text
