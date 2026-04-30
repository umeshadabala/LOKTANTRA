"""Tests for Vertex AI Service."""
import pytest
from flask import Flask
from app.services.vertex_ai_service import VertexAIService


class TestVertexAIService:
    """Test AI Service fallbacks and caching."""

    def test_init_without_app(self):
        service = VertexAIService()
        assert not service.enabled
        assert service.model is None

    def test_init_with_app_disabled(self):
        app = Flask(__name__)
        app.config['ENABLE_VERTEX_AI'] = False
        service = VertexAIService(app)
        assert not service.enabled

    def test_explain_why_static_fallback(self, app):
        """When AI is disabled, should return static content."""
        app.vertex_ai.enabled = False
        result = app.vertex_ai.explain_why(1)
        assert result['title'] == 'The Guardian of Identity'

    def test_explain_why_invalid_level(self, app):
        app.vertex_ai.enabled = False
        result = app.vertex_ai.explain_why(99)
        assert result['title'] == 'Democratic Principle'

    def test_build_prompt(self, app):
        prompt = app.vertex_ai._build_prompt(1, "test context")
        assert "Explain WHY" in prompt
        assert "test context" in prompt

    def test_cache_mechanism(self, app):
        """Test that identical requests return the exact same object from cache."""
        app.vertex_ai.enabled = True
        
        # Simulate AI generation by inserting directly into cache
        app.vertex_ai._cache = {}
        app.vertex_ai._cache[app.vertex_ai._make_cache_key(1, None)] = {'mock': 'data'}
        
        # Fetch from cache
        res = app.vertex_ai.explain_why(1)
        
        assert res == {'mock': 'data'}
        assert len(app.vertex_ai._cache) == 1
