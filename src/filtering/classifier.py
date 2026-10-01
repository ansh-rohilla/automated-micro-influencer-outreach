"""
Classifier and rule evaluation engine for influencer vetting.
"""

import re
import logging
from typing import List, Tuple
from src.filtering.criteria import FilterCriteria
from src.models.influencer import DiscoveredInfluencer, ClassificationResult, ClassifiedInfluencer

logger = logging.getLogger(__name__)


class InfluencerClassifier:
    """
    Evaluates discovered influencers against qualitative and quantitative criteria,
    computing brand fit scores and explicit pass/fail audit reasoning.
    """

    def __init__(self, criteria: FilterCriteria = None):
        self.criteria = criteria or FilterCriteria()

    def classify(self, influencer: DiscoveredInfluencer) -> ClassifiedInfluencer:
        """Evaluate a single influencer profile and return full audit classification."""
        reasons: List[str] = []
        checks = {}

        # 1. Follower Count Range Check (5,000 - 100,000)
        followers = influencer.follower_count
        if followers < self.criteria.min_followers:
            checks["follower_range_ok"] = False
            reasons.append(
                f"Follower count ({followers:,}) is below the micro-influencer threshold ({self.criteria.min_followers:,})"
            )
        elif followers > self.criteria.max_followers:
            checks["follower_range_ok"] = False
            reasons.append(
                f"Follower count ({followers:,}) exceeds the micro-influencer ceiling ({self.criteria.max_followers:,}) - classified as Macro"
            )
        else:
            checks["follower_range_ok"] = True

        # 2. Engagement Rate Check (>= 2.0%)
        er = influencer.estimated_engagement_rate
        if er < self.criteria.min_engagement_rate:
            checks["engagement_rate_ok"] = False
            reasons.append(
                f"Engagement rate ({er:.2f}%) is below minimum threshold ({self.criteria.min_engagement_rate:.1f}%)"
            )
        else:
            checks["engagement_rate_ok"] = True

        # 3. Platform Check
        platform_matched = any(
            p.lower() in influencer.primary_platform.lower() for p in self.criteria.allowed_platforms
        )
        checks["platform_ok"] = platform_matched
        if not platform_matched:
            reasons.append(f"Platform '{influencer.primary_platform}' not in allowed list")

        # 4. Brand Safety & Disqualifying Keywords
        combined_text = f"{influencer.headline} {influencer.bio} {' '.join(influencer.content_themes)}".lower()
        found_disqualifiers = [
            kw for kw in self.criteria.excluded_keywords if re.search(r'\b' + re.escape(kw) + r'\b', combined_text)
        ]
        if found_disqualifiers:
            checks["brand_safety_ok"] = False
            reasons.append(f"Contains disqualified keywords: {', '.join(found_disqualifiers)}")
        else:
            checks["brand_safety_ok"] = True

        # 5. Niche & Content Relevance Check
        matched_niche_kws = [
            kw for kw in self.criteria.target_niches if re.search(r'\b' + re.escape(kw) + r'\b', combined_text)
        ]
        niche_relevant = len(matched_niche_kws) > 0 or "tech" in influencer.category.lower()
        checks["niche_relevance_ok"] = niche_relevant
        if not niche_relevant:
            reasons.append("Content themes and bio lack direct alignment with Technology & AI niche")

        # 6. Overall Pass / Fail Decision
        all_passed = (
            checks["follower_range_ok"] and
            checks["engagement_rate_ok"] and
            checks["platform_ok"] and
            checks["brand_safety_ok"] and
            checks["niche_relevance_ok"]
        )

        # 7. Brand-Fit Score Calculation (0.0 to 10.0 scale)
        brand_score = self._compute_brand_fit_score(influencer, matched_niche_kws, checks)

        if all_passed:
            status = "PASSED"
            primary_reason = (
                f"Qualified micro-influencer: {followers:,} followers (5k-100k tier), "
                f"{er:.2f}% ER (>{self.criteria.min_engagement_rate}%), verified {influencer.category} fit."
            )
        else:
            status = "FAILED"
            primary_reason = "; ".join(reasons)

        result = ClassificationResult(
            status=status,
            brand_fit_score=brand_score,
            primary_reason=primary_reason,
            detailed_reasons=reasons if reasons else ["Met all quantitative and qualitative qualification standards."],
            criteria_checks=checks
        )

        return ClassifiedInfluencer(
            influencer=influencer,
            classification=result
        )

    def _compute_brand_fit_score(
        self,
        influencer: DiscoveredInfluencer,
        matched_kws: List[str],
        checks: dict
    ) -> float:
        """
        Calculates a 0.0 to 10.0 score reflecting campaign suitability.
        """
        score = 0.0

        # Engagement contribution (up to 4.0 pts)
        # 2.0% -> 2.0 pts; 3.0% -> 3.2 pts; 4.0%+ -> 4.0 pts
        er = influencer.estimated_engagement_rate
        score += min(4.0, (er / 4.0) * 4.0)

        # Niche relevance depth (up to 3.5 pts)
        kw_count = len(matched_kws)
        score += min(3.5, kw_count * 0.9)

        # Audience sweet spot (up to 2.5 pts)
        # Sweet spot for micro-influencers is 15k - 75k
        f = influencer.follower_count
        if 15_000 <= f <= 75_000:
            score += 2.5
        elif 5_000 <= f < 15_000 or 75_000 < f <= 100_000:
            score += 1.8
        else:
            score += 0.5  # Nano or Macro penalty

        return round(min(10.0, max(1.0, score)), 1)
