"""
API Routes — Vertex AI explanations and player progress.

Provides endpoints for:
- AI-grounded 'Why' explanations via Vertex AI or static fallback.
- Player session progress persistence.
"""
import logging
from typing import Tuple, Union, Optional
from flask import Blueprint, jsonify, request, current_app, Response
from app.utils import (
    validate_level_id, validate_session_id, sanitize_text,
)

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)


@api_bp.route('/explain', methods=['POST'])
def explain_why() -> Union[Response, Tuple[Response, int]]:
    """
    Get AI-grounded 'Why' explanation for a level.

    Expected JSON body:
        level_id (int): Level number between 1 and 8.
        context (str, optional): Additional player context.
        player_id (str, optional): Unique player identifier.

    Returns:
        JSON with 'explanation', 'level_id', and 'source'.

    Status Codes:
        200: Explanation generated successfully.
        400: Invalid or missing request data.
    """
    data: Optional[dict] = request.get_json()
    if not data:
        logger.warning("Explain request received with no JSON body")
        return jsonify({'error': 'No data provided'}), 400

    level_id = data.get('level_id')
    if not validate_level_id(level_id):
        logger.warning("Invalid level_id in explain request: %s", level_id)
        return jsonify({'error': 'Valid level_id (1-8) is required'}), 400

    context = sanitize_text(data.get('context', ''), max_length=500) or None
    player_id = sanitize_text(data.get('player_id', 'anonymous'))

    explanation = current_app.vertex_ai.explain_why(level_id, context)
    source = 'vertex_ai' if current_app.vertex_ai.enabled else 'static'

    current_app.cloud_logger.log_ai_explanation(player_id, level_id, source)
    logger.info(
        "Explanation served: level=%d source=%s player=%s",
        level_id, source, player_id,
    )

    return jsonify({
        'explanation': explanation,
        'level_id': level_id,
        'source': source,
    })


@api_bp.route('/progress/<session_id>')
def get_progress(session_id: str) -> Response:
    """
    Get player progress for a session.

    Args:
        session_id: The unique session identifier from the URL path.

    Returns:
        JSON with 'progress' data and 'exists' boolean flag.
    """
    if not validate_session_id(session_id):
        return jsonify({'progress': None, 'exists': False})

    progress = current_app.firestore.get_progress(session_id)
    if not progress:
        return jsonify({'progress': None, 'exists': False})
    return jsonify({'progress': progress, 'exists': True})


@api_bp.route('/progress', methods=['POST'])
def save_progress() -> Union[Response, Tuple[Response, int]]:
    """
    Save player progress for a session.

    Expected JSON body:
        session_id (str): Unique session identifier.
        levels (dict): Per-level progress data.
        current_level (int): Current level index.

    Returns:
        JSON with 'success' flag and saved 'record'.

    Status Codes:
        200: Progress saved successfully.
        400: Invalid or missing request data.
    """
    data: Optional[dict] = request.get_json()
    if not data:
        logger.warning("Save progress request with no JSON body")
        return jsonify({'error': 'No data provided'}), 400

    session_id = data.get('session_id', '')
    if not validate_session_id(session_id):
        logger.warning("Invalid session_id in progress save: %s", session_id)
        return jsonify({'error': 'session_id required'}), 400

    record = current_app.firestore.save_progress(session_id, data)
    logger.info("Progress saved for session: %s", session_id)
    return jsonify({'success': True, 'record': record}), 200
