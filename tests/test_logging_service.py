"""Tests for Logging Service."""
import pytest
from flask import Flask
from app.services.logging_service import LoggingService

class TestLoggingService:
    def test_init_without_app(self):
        service = LoggingService()
        assert not service.enabled
        assert service.client is None

    def test_init_with_app_disabled(self):
        app = Flask(__name__)
        app.config['ENABLE_CLOUD_LOGGING'] = False
        service = LoggingService(app)
        assert not service.enabled

    def test_log_level_started(self, app):
        app.cloud_logger.enabled = False
        # Should not raise exception
        app.cloud_logger.log_level_started("p1", 1)

    def test_log_level_completed(self, app):
        app.cloud_logger.enabled = False
        app.cloud_logger.log_level_completed(
            player_id="p1", level_id=1, score=100, duration_seconds=60, stars=3
        )

    def test_log_score_submitted(self, app):
        app.cloud_logger.enabled = False
        app.cloud_logger.log_score_submitted("Player1", 800, 8)

    def test_log_ai_explanation(self, app):
        app.cloud_logger.enabled = False
        app.cloud_logger.log_ai_explanation("p1", 1, "static")
