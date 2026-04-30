"""
Firestore Service — Global Civic Leaderboard & Player Progress
Uses google-cloud-firestore for persistence with in-memory fallback.
"""
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from flask import Flask

logger = logging.getLogger(__name__)


class FirestoreService:
    """Manages leaderboard and player progress via Cloud Firestore with fallback support."""

    def __init__(self, app: Optional[Flask] = None):
        self.client: Any = None
        self.enabled: bool = False
        self._memory_leaderboard: List[Dict[str, Any]] = []
        self._memory_progress: Dict[str, Any] = {}

        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize Firestore client if enabled in configuration.

        Args:
            app: The Flask application instance.
        """
        self.leaderboard_collection = app.config.get(
            'FIRESTORE_COLLECTION_LEADERBOARD', 'leaderboard')
        self.progress_collection = app.config.get(
            'FIRESTORE_COLLECTION_PROGRESS', 'player_progress')

        if app.config.get('ENABLE_FIRESTORE'):
            try:
                from google.cloud import firestore  # pylint: disable=import-outside-toplevel,import-error
                project_id = app.config.get('GCP_PROJECT_ID')
                self.client = firestore.Client(project=project_id)
                self.enabled = True
                logger.info("Firestore initialized for project: %s", project_id)
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.warning("Firestore unavailable, using in-memory fallback: %s", e)
                self.enabled = False
        else:
            logger.info("Firestore disabled, using in-memory storage")

    # ── Leaderboard Operations ──────────────────────────────────────

    def save_score(self,
                   player_name: str,
                   total_score: int,
                   levels_completed: int,
                   **kwargs: Any) -> Dict[str, Any]:
        """
        Save a player's score with saga-specific breakdowns.

        Args:
            player_name: Name of the player.
            total_score: Total score achieved.
            levels_completed: Number of levels finished.
            **kwargs: Additional data including email, age, saga_type, voter_score, officer_score.

        Returns:
            The saved entry dictionary.
        """
        email = kwargs.get('email', '')
        doc_id = email.replace('@', '_').replace('.', '_') if email else str(uuid.uuid4())

        entry = {
            'id': doc_id,
            'player_name': player_name,
            'age': kwargs.get('age', 0),
            'email': email,
            'total_score': total_score,
            'voter_score': kwargs.get('voter_score', 0),
            'officer_score': kwargs.get('officer_score', 0),
            'levels_completed': levels_completed,
            'saga_type': kwargs.get('saga_type', 'both'),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'updated_at': time.time(),
        }

        if self.enabled and self.client:
            try:
                doc_ref = self.client.collection(self.leaderboard_collection).document(doc_id)
                doc_ref.set(entry, merge=True)
                return entry
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.error("Firestore save_score failed: %s", e)

        # In-memory fallback
        existing_idx = next(
            (i for i, e in enumerate(self._memory_leaderboard)
             if e.get('email') == email), -1
        )
        if existing_idx >= 0:
            self._memory_leaderboard[existing_idx] = entry
        else:
            self._memory_leaderboard.append(entry)
        return entry

    def get_top_scores(
        self, limit: int = 50, saga_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve top scores, sorting by relevant saga score if filtered.

        Args:
            limit: Maximum number of scores to retrieve.
            saga_filter: Optional saga type to filter by.

        Returns:
            A list of score entries.
        """
        if self.enabled and self.client:
            return self._get_scores_from_firestore(limit, saga_filter)
        return self._get_scores_from_memory(limit, saga_filter)

    def _get_scores_from_firestore(
        self, limit: int, saga_filter: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Helper to fetch scores from Firestore."""
        sort_field = self._get_sort_field(saga_filter)
        try:
            query = self.client.collection(self.leaderboard_collection) \
                .order_by(sort_field, direction='DESCENDING') \
                .limit(limit)

            if saga_filter and saga_filter != 'both':
                query = query.where(saga_filter + '_score', '>', 0)

            docs = query.stream()
            return [ {**doc.to_dict(), 'id': doc.id} for doc in docs ]
        except Exception as e: # pylint: disable=broad-exception-caught
            logger.error("Firestore get_top_scores failed: %s", e)
            return []

    def _get_scores_from_memory(
        self, limit: int, saga_filter: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Helper to fetch scores from in-memory storage."""
        sort_field = self._get_sort_field(saga_filter)
        entries = self._memory_leaderboard
        if saga_filter and saga_filter != 'both':
            entries = [e for e in entries if e.get(saga_filter + '_score', 0) > 0]

        entries.sort(key=lambda x: x.get(sort_field, 0), reverse=True)
        return entries[:limit]

    def _get_sort_field(self, saga_filter: Optional[str]) -> str:
        """Helper to determine the sort field."""
        if saga_filter == 'voter':
            return 'voter_score'
        if saga_filter == 'officer':
            return 'officer_score'
        return 'total_score'

    # ── Progress Operations ─────────────────────────────────────────

    def save_progress(self, session_id: str, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save player progress for a session.

        Args:
            session_id: The unique session identifier.
            progress_data: The progress data to save.

        Returns:
            The saved record dictionary.
        """
        record = {
            'session_id': session_id,
            'levels': progress_data.get('levels', {}),
            'current_level': progress_data.get('current_level', 1),
            'total_score': progress_data.get('total_score', 0),
            'updated_at': datetime.now(timezone.utc).isoformat(),
        }

        if self.enabled and self.client:
            try:
                doc_ref = self.client.collection(self.progress_collection).document(session_id)
                doc_ref.set(record, merge=True)
                logger.info("Progress saved to Firestore: session %s", session_id)
                return record
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.error("Firestore save_progress failed: %s", e)

        # In-memory fallback
        self._memory_progress[session_id] = record
        return record

    def get_progress(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve player progress for a session.

        Args:
            session_id: The unique session identifier.

        Returns:
            The progress data dictionary if found, else None.
        """
        if self.enabled and self.client:
            try:
                doc_ref = self.client.collection(self.progress_collection).document(session_id)
                doc = doc_ref.get()
                if doc.exists:
                    return doc.to_dict()
                return None
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.error("Firestore get_progress failed: %s", e)

        # In-memory fallback
        return self._memory_progress.get(session_id)

    def clear_progress(self, session_id: str) -> bool:
        """
        Clear player progress for a session.

        Args:
            session_id: The unique session identifier.

        Returns:
            True if cleared successfully.
        """
        if self.enabled and self.client:
            try:
                self.client.collection(self.progress_collection).document(session_id).delete()
                return True
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.error("Firestore clear_progress failed: %s", e)

        self._memory_progress.pop(session_id, None)
        return True
