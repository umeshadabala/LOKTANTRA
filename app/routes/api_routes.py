"""API Routes — Vertex AI explanations and player progress."""
from typing import Any, Dict, Tuple, Union, Optional
from flask import Blueprint, jsonify, request, current_app, Response

api_bp = Blueprint('api', __name__)


@api_bp.route('/explain', methods=['POST'])
def explain_why() -> Union[Response, Tuple[Response, int]]:
    """
    Get AI-grounded 'Why' explanation for a level.

    Expected JSON body:
        level_id (int): 1-8
        context (str, optional): Additional player context
        player_id (str, optional): Unique player identifier

    Returns:
        JSON response with the explanation and source.
    """
    data: Optional[Dict[str, Any]] = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    level_id = data.get('level_id')
    if not level_id or not isinstance(level_id, int) or level_id < 1 or level_id > 8:
        return jsonify({'error': 'Valid level_id (1-8) is required'}), 400

    context = data.get('context')
    player_id = data.get('player_id', 'anonymous')

    explanation = current_app.vertex_ai.explain_why(level_id, context)

    source = 'vertex_ai' if current_app.vertex_ai.enabled else 'static'
    current_app.cloud_logger.log_ai_explanation(player_id, level_id, source)

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
        session_id: The unique session identifier.

    Returns:
        JSON response with progress data.
    """
    progress = current_app.firestore.get_progress(session_id)
    if not progress:
        return jsonify({'progress': None, 'exists': False})
    return jsonify({'progress': progress, 'exists': True})


@api_bp.route('/progress', methods=['POST'])
def save_progress() -> Union[Response, Tuple[Response, int]]:
    """
    Save player progress for a session.

    Expected JSON body:
        session_id (str): Unique session identifier
        levels (dict): Per-level progress data
        current_level (int): Current level index

    Returns:
        JSON response indicating success.
    """
    data: Optional[Dict[str, Any]] = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    session_id = data.get('session_id')
    if not session_id:
        return jsonify({'error': 'session_id required'}), 400

    record = current_app.firestore.save_progress(session_id, data)
    return jsonify({'success': True, 'record': record}), 200
