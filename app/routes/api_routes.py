"""API Routes — Vertex AI explanations and player progress."""
from flask import Blueprint, jsonify, request, current_app

api_bp = Blueprint('api', __name__)


@api_bp.route('/explain', methods=['POST'])
def explain_why():
    """Get AI-grounded 'Why' explanation for a level."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    level_id = data.get('level_id')
    if not level_id or not isinstance(level_id, int) or level_id < 1 or level_id > 8:
        return jsonify({'error': 'Valid level_id (1-8) is required'}), 400

    context = data.get('context', None)
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
def get_progress(session_id):
    """Get player progress for a session."""
    progress = current_app.firestore.get_progress(session_id)
    if not progress:
        return jsonify({'progress': None, 'exists': False})
    return jsonify({'progress': progress, 'exists': True})


@api_bp.route('/progress', methods=['POST'])
def save_progress():
    """Save player progress."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    session_id = data.get('session_id')
    if not session_id:
        return jsonify({'error': 'session_id required'}), 400

    record = current_app.firestore.save_progress(session_id, data)
    return jsonify({'success': True, 'record': record}), 200
