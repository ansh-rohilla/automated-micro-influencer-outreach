"""
AI Message Personalization package.
"""

from src.personalization.generator import PersonalizationEngine
from src.personalization.pipeline import PersonalizationPipeline
from src.personalization.prompts import (
    EMAIL_PITCH_PROMPT_TEMPLATE,
    INSTAGRAM_DM_PROMPT_TEMPLATE,
    COLLABORATION_ANGLES,
)

__all__ = [
    "PersonalizationEngine",
    "PersonalizationPipeline",
    "EMAIL_PITCH_PROMPT_TEMPLATE",
    "INSTAGRAM_DM_PROMPT_TEMPLATE",
    "COLLABORATION_ANGLES",
]
