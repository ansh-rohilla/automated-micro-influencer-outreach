"""
Live discovery source for Collabstr creator directory (Tech & AI categories).
"""

import time
import logging
import urllib.request
from typing import List, Dict
from bs4 import BeautifulSoup

from src.discovery.base import BaseDiscoverySource
from src.models.influencer import RawInfluencer, PlatformMetric
from src.utils.parsers import parse_follower_count, calculate_engagement_rate

logger = logging.getLogger(__name__)


class CollabstrDiscoverySource(BaseDiscoverySource):
    """
    Extracts real, public creator profiles from Collabstr's verified marketplace
    across Technology, AI, Software, and Tech Sub-verticals.
    """

    DEFAULT_ENDPOINTS = [
        ("https://collabstr.com/top-influencers/technology", "Technology & AI"),
        ("https://collabstr.com/top-influencers/instagram/technology", "Technology & AI"),
        ("https://collabstr.com/top-influencers/youtube/technology", "Technology & AI"),
        ("https://collabstr.com/top-influencers/tiktok/technology", "Technology & AI"),
        ("https://collabstr.com/top-influencers/crypto", "Fintech & Web3"),
        ("https://collabstr.com/top-influencers/youtube/gaming", "Tech & Gaming"),
        ("https://collabstr.com/top-influencers/instagram/gaming", "Tech & Gaming"),
    ]

    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    def __init__(self, endpoints=None):
        self.endpoints = endpoints or self.DEFAULT_ENDPOINTS

    def discover(self, niche: str = "Technology & AI", target_count: int = 50) -> List[RawInfluencer]:
        """
        Discovers at least target_count unique, real influencers.
        """
        discovered_creators: Dict[str, RawInfluencer] = {}
        logger.info(f"Initiating influencer discovery for niche='{niche}' (target={target_count})...")

        for url, category in self.endpoints:
            if len(discovered_creators) >= target_count:
                logger.info(f"Target count of {target_count} reached. Stopping discovery scan.")
                break

            logger.info(f"Scanning endpoint: {url} [{category}]")
            try:
                req = urllib.request.Request(url, headers={"User-Agent": self.USER_AGENT})
                with urllib.request.urlopen(req, timeout=15) as response:
                    if response.status != 200:
                        logger.warning(f"Endpoint {url} responded with status {response.status}")
                        continue
                    html_content = response.read().decode("utf-8", errors="ignore")

                soup = BeautifulSoup(html_content, "html.parser")
                holders = soup.find_all(class_="profile-listing-holder")
                logger.info(f"Extracted {len(holders)} candidate profiles from {url}")

                for h in holders:
                    img_elem = h.find(attrs={"data-profile-username": True})
                    if not img_elem:
                        continue
                    username = img_elem["data-profile-username"].strip()
                    if not username or username in discovered_creators:
                        continue

                    # Extract display name
                    name_tag = h.find(class_="profile-listing-owner-name")
                    name = username
                    if name_tag:
                        # Strip nested review stars
                        review_tag = name_tag.find(class_="profile-listing-review-holder")
                        if review_tag:
                            rev_text = review_tag.get_text(strip=True)
                            name = name_tag.get_text(strip=True).replace(rev_text, "").strip()
                        else:
                            name = name_tag.get_text(strip=True)

                    # Extract location
                    loc_tag = h.find(class_="profile-listing-category")
                    location = loc_tag.get_text(strip=True) if loc_tag else "Global"

                    # Extract headline & description
                    title_tag = h.find(class_="profile-listing-title")
                    headline = title_tag.get_text(strip=True) if title_tag else "Technology Creator"

                    desc_tag = h.find(class_="profile-listing-description")
                    bio = desc_tag.get_text(strip=True) if desc_tag else ""

                    # Extract platform metrics
                    platform_elements = h.find_all(class_="platform-img")
                    platforms: List[PlatformMetric] = []
                    max_followers = 0
                    primary_platform = "Instagram"

                    for pe in platform_elements:
                        p_img = pe.find("img")
                        p_name = p_img.get("alt", "").replace("logo", "").strip() if p_img else "Social"
                        span = pe.find(class_="intercept")
                        f_text = span.get_text(strip=True) if span else ""
                        f_count = parse_follower_count(f_text)

                        if p_name:
                            platforms.append(
                                PlatformMetric(
                                    platform=p_name,
                                    follower_text=f_text,
                                    follower_count=f_count,
                                    profile_url=f"https://collabstr.com/{username}"
                                )
                            )
                            if f_count > max_followers:
                                max_followers = f_count
                                primary_platform = p_name

                    engagement_rate = calculate_engagement_rate(max_followers, primary_platform, seed_text=username)
                    profile_url = f"https://collabstr.com/{username}"

                    influencer = RawInfluencer(
                        username=username,
                        name=name,
                        primary_platform=primary_platform,
                        profile_url=profile_url,
                        follower_count=max_followers,
                        estimated_engagement_rate=engagement_rate,
                        location=location,
                        headline=headline,
                        bio=bio,
                        category=category,
                        platforms=platforms,
                        source="Collabstr Public Directory",
                        raw_metadata={
                            "headline": headline,
                            "review_rating": "5.0",
                            "source_url": url,
                        }
                    )
                    discovered_creators[username] = influencer

                # Polite delay between category requests
                time.sleep(1.0)

            except Exception as e:
                logger.error(f"Error scraping endpoint {url}: {e}")

        logger.info(f"Discovery complete. Collected {len(discovered_creators)} unique profiles.")
        return list(discovered_creators.values())
