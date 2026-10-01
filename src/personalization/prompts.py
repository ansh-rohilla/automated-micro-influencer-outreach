"""
Prompt definitions and templates for AI message personalization.
"""

EMAIL_PITCH_PROMPT_TEMPLATE = """You are a senior brand partnerships manager reaching out to a technology micro-influencer for a collaboration.

Influencer Profile:
- Name: {name}
- Handle: {username}
- Primary Platform: {platform} ({follower_count:,} followers, {engagement_rate}% ER)
- Niche & Themes: {category} ({themes})
- Tone/Style: {tone_style}
- Recent Topics: {recent_topics}
- Audience: {audience_demo} in {location}
- Proposed Collaboration Angle: {angle}
- Brand Value Proposition: {value_prop}

Requirements for Email Pitch:
1. Length: STRICTLY 60 to 90 words (inclusive). Count every single word.
2. Tone: Professional, authentic, peer-to-peer.
3. Specificity: Reference their specific recent content/niche ({recent_topics}) and audience fit.
4. Call to action: Low-friction ask (e.g. quick 10-min chat or brief feedback).
5. Do NOT include markdown placeholders or generic copy.

Write the personalized Email Pitch (Subject line on line 1, then body):"""

INSTAGRAM_DM_PROMPT_TEMPLATE = """You are reaching out via Instagram DM to {name} (@{username}), a {category} creator.

Creator Context:
- Recent Content: {recent_topics}
- Platform: {platform}
- Audience: {audience_demo}
- Proposed Angle: {angle}

Requirements for Instagram DM:
1. Length: STRICTLY 15 to 30 words (inclusive).
2. Style: Casual, friendly, direct, natural — like a real human DM, not a sales pitch.
3. Reference: Mention liking their recent content on {recent_topics}.
4. No hashtags, no excessive punctuation.

Write only the DM text:"""

COLLABORATION_ANGLES = [
    "Sponsorship",
    "Affiliate campaign",
    "UGC content creation",
    "Brand ambassador program",
    "Paid product placement",
    "Barter collaboration"
]
