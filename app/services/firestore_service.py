"""
Firestore Service — Global Civic Leaderboard & Player Progress
Uses google-cloud-firestore for persistence with in-memory fallback.
"""
import logging
import time
import uuid
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class FirestoreService:
    """Manages leaderboard and player progress via Cloud Firestore."""

    def __init__(self, app=None):
        self.client = None
        self.enabled = False
        self._memory_leaderboard = []
        self._memory_progress = {}

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Firestore client if enabled."""
        self.leaderboard_collection = app.config.get(
            'FIRESTORE_COLLECTION_LEADERBOARD', 'leaderboard')
        self.progress_collection = app.config.get(
            'FIRESTORE_COLLECTION_PROGRESS', 'player_progress')

        if app.config.get('ENABLE_FIRESTORE'):
            try:
                from google.cloud import firestore
                project_id = app.config.get('GCP_PROJECT_ID')
                self.client = firestore.Client(project=project_id)
                self.enabled = True
                logger.info("Firestore initialized for project: %s", project_id)
            except Exception as e:
                logger.warning("Firestore unavailable, using in-memory fallback: %s", e)
                self.enabled = False
        else:
            logger.info("Firestore disabled, using in-memory storage")

    # ── Leaderboard Operations ──────────────────────────────────────

    def save_score(self, player_name, total_score, levels_completed, saga_type='both', age=0, email='', voter_score=0, officer_score=0):
        """Save a player's score with saga-specific breakdowns."""
        doc_id = email.replace('@', '_').replace('.', '_') if email else str(uuid.uuid4())
        
        entry = {
            'id': doc_id,
            'player_name': player_name,
            'age': age,
            'email': email,
            'total_score': total_score,
            'voter_score': voter_score,
            'officer_score': officer_score,
            'levels_completed': levels_completed,
            'saga_type': saga_type,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'updated_at': time.time(),
        }

        if self.enabled and self.client:
            try:
                doc_ref = self.client.collection(self.leaderboard_collection).document(doc_id)
                doc_ref.set(entry, merge=True)
                return entry
            except Exception as e:
                logger.error("Firestore save_score failed: %s", e)

        # In-memory fallback
        existing_idx = next((i for i, e in enumerate(self._memory_leaderboard) if e.get('email') == email), -1)
        if existing_idx >= 0:
            self._memory_leaderboard[existing_idx] = entry
        else:
            self._memory_leaderboard.append(entry)
        return entry

    def get_top_scores(self, limit=50, saga_filter=None):
        """Retrieve top scores, sorting by relevant saga score if filtered."""
        sort_field = 'total_score'
        if saga_filter == 'voter':
            sort_field = 'voter_score'
        elif saga_filter == 'officer':
            sort_field = 'officer_score'

        if self.enabled and self.client:
            try:
                query = self.client.collection(self.leaderboard_collection) \
                    .order_by(sort_field, direction='DESCENDING') \
                    .limit(limit)

                if saga_filter and saga_filter != 'both':
                    # Only show players who have actually played this saga
                    query = query.where(saga_filter + '_score', '>', 0)

                docs = query.stream()
                return [ {**doc.to_dict(), 'id': doc.id} for doc in docs ]
            except Exception as e:
                logger.error("Firestore get_top_scores failed: %s", e)

        # In-memory fallback
        entries = self._memory_leaderboard
        if saga_filter and saga_filter != 'both':
            entries = [e for e in entries if e.get(saga_filter + '_score', 0) > 0]
            entries.sort(key=lambda x: x.get(sort_field, 0), reverse=True)
        else:
            entries.sort(key=lambda x: x.get('total_score', 0), reverse=True)
            
        return entries[:limit]

    # ── Progress Operations ─────────────────────────────────────────

    def save_progress(self, session_id, progress_data):
        """Save player progress for a session."""
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
            except Exception as e:
                logger.error("Firestore save_progress failed: %s", e)

        # In-memory fallback
        self._memory_progress[session_id] = record
        return record

    def get_progress(self, session_id):
        """Retrieve player progress for a session."""
        if self.enabled and self.client:
            try:
                doc_ref = self.client.collection(self.progress_collection).document(session_id)
                doc = doc_ref.get()
                if doc.exists:
                    return doc.to_dict()
                return None
            except Exception as e:
                logger.error("Firestore get_progress failed: %s", e)

        # In-memory fallback
        return self._memory_progress.get(session_id)

    def clear_progress(self, session_id):
        """Clear player progress for a session."""
        if self.enabled and self.client:
            try:
                self.client.collection(self.progress_collection).document(session_id).delete()
                return True
            except Exception as e:
                logger.error("Firestore clear_progress failed: %s", e)

        self._memory_progress.pop(session_id, None)
        return True
