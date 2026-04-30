"""Tests for Vertex AI Service (static fallback mode)."""
import pytest


class TestVertexAIFallback:
    """Test Vertex AI service in offline/static mode."""

    def test_explain_level_1(self, app):
        result = app.vertex_ai.explain_why(1)
        assert 'title' in result
        assert 'explanation' in result
        assert 'article_reference' in result
        assert 'fun_fact' in result
        assert 'Ghost Voting' in result['explanation'] or 'Electoral Roll' in result['explanation']

    def test_explain_all_levels(self, app):
        for level_id in range(1, 9):
            result = app.vertex_ai.explain_why(level_id)
            assert result['title'], f"Missing title for level {level_id}"
            assert len(result['explanation']) > 50, f"Explanation too short for level {level_id}"

    def test_explain_invalid_level(self, app):
        result = app.vertex_ai.explain_why(99)
        assert 'title' in result  # Falls back to generic

    def test_caching(self, app):
        r1 = app.vertex_ai.explain_why(1)
        r2 = app.vertex_ai.explain_why(1)
        assert r1 == r2  # Should return cached result

    def test_explain_with_context(self, app):
        result = app.vertex_ai.explain_why(1, context="Player found 5/7 voters")
        assert result is not None

    def test_service_disabled(self, app):
        assert app.vertex_ai.enabled is False  # Testing config disables it
