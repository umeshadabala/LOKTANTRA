"""
Input Sanitization Utilities

Provides reusable input validation and sanitization functions
for all route handlers to prevent injection attacks and ensure
data integrity across the application.
"""
import re
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Compiled regex patterns for performance
_EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)
_SAFE_TEXT_PATTERN = re.compile(r'^[\w\s\-.,!?@#()\'\"]+$')

# Application constants
MIN_PLAYER_AGE = 18
MAX_PLAYER_AGE = 120
MIN_LEVEL_ID = 1
MAX_LEVEL_ID = 8
MAX_NAME_LENGTH = 100
MAX_SESSION_ID_LENGTH = 128
MAX_SCORE_PER_LEVEL = 100
MAX_TOTAL_SCORE = 800


def sanitize_text(value: Any, max_length: int = 200) -> str:
    """
    Sanitize a text input by stripping whitespace and truncating.

    Args:
        value: The raw input value to sanitize.
        max_length: Maximum allowed length after sanitization.

    Returns:
        A sanitized string, or empty string if input is invalid.
    """
    if not isinstance(value, str):
        return ''
    cleaned = value.strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned


def validate_email(email: str) -> bool:
    """
    Validate an email address format.

    Args:
        email: The email address to validate.

    Returns:
        True if the email format is valid, False otherwise.
    """
    if not email or len(email) > 254:
        return False
    return bool(_EMAIL_PATTERN.match(email))


def validate_level_id(level_id: Any) -> bool:
    """
    Validate that a level ID is within the valid range (1-8).

    Args:
        level_id: The level ID to validate.

    Returns:
        True if the level ID is valid.
    """
    return (
        isinstance(level_id, int)
        and MIN_LEVEL_ID <= level_id <= MAX_LEVEL_ID
    )


def validate_player_age(age: Any) -> bool:
    """
    Validate that the player age is within acceptable bounds.

    Args:
        age: The age value to validate.

    Returns:
        True if the age is valid for a citizen voter (18-120).
    """
    return (
        isinstance(age, int)
        and MIN_PLAYER_AGE <= age <= MAX_PLAYER_AGE
    )


def validate_session_id(session_id: Any) -> bool:
    """
    Validate a session ID for format and length.

    Args:
        session_id: The session ID to validate.

    Returns:
        True if the session ID is valid.
    """
    if not isinstance(session_id, str):
        return False
    stripped = session_id.strip()
    return 0 < len(stripped) <= MAX_SESSION_ID_LENGTH


def validate_score(score: Any, max_value: int = MAX_TOTAL_SCORE) -> int:
    """
    Validate and clamp a score value to acceptable bounds.

    Args:
        score: The raw score value.
        max_value: The maximum allowed score.

    Returns:
        A validated integer score clamped between 0 and max_value.
    """
    if not isinstance(score, (int, float)):
        return 0
    return max(0, min(int(score), max_value))
