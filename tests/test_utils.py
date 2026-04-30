"""Tests for input sanitization utilities."""
import pytest
from app.utils import (
    sanitize_text, validate_email, validate_level_id,
    validate_player_age, validate_session_id, validate_score,
)


class TestSanitizeText:
    """Test text sanitization and truncation."""

    def test_strips_whitespace(self):
        assert sanitize_text('  hello  ') == 'hello'

    def test_truncates_long_input(self):
        result = sanitize_text('a' * 300, max_length=100)
        assert len(result) == 100

    def test_returns_empty_for_non_string(self):
        assert sanitize_text(123) == ''
        assert sanitize_text(None) == ''

    def test_preserves_valid_text(self):
        assert sanitize_text('Valid Name') == 'Valid Name'


class TestValidateEmail:
    """Test email format validation."""

    def test_valid_email(self):
        assert validate_email('user@example.com') is True

    def test_invalid_email_no_at(self):
        assert validate_email('userexample.com') is False

    def test_invalid_email_empty(self):
        assert validate_email('') is False

    def test_invalid_email_too_long(self):
        assert validate_email('a' * 250 + '@b.com') is False

    def test_invalid_email_none(self):
        assert validate_email(None) is False


class TestValidateLevelId:
    """Test level ID range validation."""

    def test_valid_levels(self):
        for i in range(1, 9):
            assert validate_level_id(i) is True

    def test_invalid_zero(self):
        assert validate_level_id(0) is False

    def test_invalid_nine(self):
        assert validate_level_id(9) is False

    def test_invalid_string(self):
        assert validate_level_id('1') is False

    def test_invalid_none(self):
        assert validate_level_id(None) is False


class TestValidatePlayerAge:
    """Test player age bounds validation."""

    def test_valid_age(self):
        assert validate_player_age(18) is True
        assert validate_player_age(65) is True
        assert validate_player_age(120) is True

    def test_underage(self):
        assert validate_player_age(17) is False

    def test_overage(self):
        assert validate_player_age(121) is False

    def test_non_integer(self):
        assert validate_player_age('18') is False


class TestValidateSessionId:
    """Test session ID format validation."""

    def test_valid_session(self):
        assert validate_session_id('abc123') is True

    def test_empty_string(self):
        assert validate_session_id('') is False

    def test_too_long(self):
        assert validate_session_id('x' * 200) is False

    def test_non_string(self):
        assert validate_session_id(123) is False


class TestValidateScore:
    """Test score clamping and validation."""

    def test_valid_score(self):
        assert validate_score(500) == 500

    def test_negative_clamped_to_zero(self):
        assert validate_score(-10) == 0

    def test_over_max_clamped(self):
        assert validate_score(9999, max_value=800) == 800

    def test_non_numeric_returns_zero(self):
        assert validate_score('abc') == 0

    def test_float_converted(self):
        assert validate_score(99.7) == 99
