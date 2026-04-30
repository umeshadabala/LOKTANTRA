"""
Cloud Logging Service — Audit Trail for Level Events
Uses google-cloud-logging for structured event logging.
"""
import logging
import json
from datetime import datetime, timezone
from typing import Any, Optional
from flask import Flask

logger = logging.getLogger(__name__)


class LoggingService:
    """Manages structured audit logging for election simulation events."""

    def __init__(self, app: Optional[Flask] = None):
        self.client: Any = None
        self.enabled: bool = False
        self.log_name: str = "loktantra-audit-trail"

        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize Cloud Logging client if enabled in configuration.

        Args:
            app: The Flask application instance.
        """
        self.log_name = app.config.get('CLOUD_LOGGING_NAME', 'loktantra-audit-trail')

        if app.config.get('ENABLE_CLOUD_LOGGING'):
            try:
                from google.cloud import logging as cloud_logging
                self.client = cloud_logging.Client(
                    project=app.config.get('GCP_PROJECT_ID')
                )
                self.enabled = True
                logger.info("Cloud Logging initialized: %s", self.log_name)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("Cloud Logging unavailable, using local stdout: %s", e)
                self.enabled = False
        else:
            logger.info("Cloud Logging disabled, using local stdout")

    def log_event(self, event_type: str, data: Any) -> None:
        """
        Log a structured event to Cloud Logging or local stdout.

        Args:
            event_type: The category of the event.
            data: The event payload (dict or serializable object).
        """
        payload = {
            'event_type': event_type,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'data': data
        }

        if self.enabled and self.client:
            try:
                logging_handler = self.client.logger(self.log_name)
                logging_handler.log_struct(payload, severity="INFO")
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("Cloud Logging failed: %s", e)
                # Fallback to local
                print(json.dumps(payload))
        else:
            # Local development logging
            logger.debug("Local Event [%s]: %s", event_type, data)

    def log_level_started(self, player_id: str, level_id: int) -> None:
        """Audit when a player begins a level."""
        self.log_event('level_started', {'player_id': player_id, 'level_id': level_id})

    def log_level_completed(self,
                           player_id: str,
                           level_id: int,
                           score: int,
                           duration_seconds: int,
                           stars: int) -> None:
        """Audit when a player finishes a level with results."""
        self.log_event('level_completed', {
            'player_id': player_id,
            'level_id': level_id,
            'score': score,
            'duration_seconds': duration_seconds,
            'stars': stars
        })

    def log_score_submitted(self, player_name: str, total_score: int, levels: int) -> None:
        """Audit when a final score is submitted to the leaderboard."""
        self.log_event('score_submitted', {
            'player_name': player_name,
            'total_score': total_score,
            'levels_completed': levels
        })

    def log_ai_explanation(self, level_id: int, prompt: str) -> None:
        """Audit AI explanation requests for transparency."""
        self.log_event('ai_explanation_request', {
            'level_id': level_id,
            'prompt_summary': prompt[:100]
        })
