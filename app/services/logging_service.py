"""
Cloud Logging Service — Audit Trail for Level Events
Uses google-cloud-logging for structured event logging.
"""
import logging
import json
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class LoggingService:
    """Structured logging for game events via Google Cloud Logging."""

    def __init__(self, app=None):
        self.cloud_logger = None
        self.enabled = False
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Cloud Logging if enabled."""
        if app.config.get('ENABLE_CLOUD_LOGGING'):
            try:
                import google.cloud.logging as cloud_logging
                project_id = app.config.get('GCP_PROJECT_ID')
                client = cloud_logging.Client(project=project_id)
                client.setup_logging()
                self.cloud_logger = client.logger('loktantra-game-events')
                self.enabled = True
                logger.info("Cloud Logging initialized for project: %s", project_id)
            except Exception as e:
                logger.warning("Cloud Logging unavailable: %s", e)
                self.enabled = False
        else:
            logger.info("Cloud Logging disabled, using standard logging")

    def log_event(self, event_type, data=None):
        """Log a structured game event."""
        payload = {
            'event_type': event_type,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'data': data or {},
        }
        if self.enabled and self.cloud_logger:
            try:
                self.cloud_logger.log_struct(payload, severity='INFO',
                    labels={'app': 'loktantra', 'event': event_type})
            except Exception as e:
                logger.error("Cloud Logging failed: %s", e)
        logger.info("GAME_EVENT [%s]: %s", event_type, json.dumps(payload, default=str))

    def log_level_started(self, player_id, level_id):
        self.log_event('level_started', {'player_id': player_id, 'level_id': level_id})

    def log_level_completed(self, player_id, level_id, score, duration_seconds, stars):
        self.log_event('level_completed', {
            'player_id': player_id, 'level_id': level_id,
            'score': score, 'duration_seconds': duration_seconds, 'stars': stars,
        })

    def log_score_submitted(self, player_name, total_score, levels_completed):
        self.log_event('score_submitted', {
            'player_name': player_name, 'total_score': total_score,
            'levels_completed': levels_completed,
        })

    def log_ai_explanation(self, player_id, level_id, source):
        self.log_event('ai_explanation_requested', {
            'player_id': player_id, 'level_id': level_id, 'source': source,
        })
