"""Leaderboard Routes — Global Civic Leaderboard endpoints."""
from typing import Any, Dict, Tuple, Union, Optional
from flask import Blueprint, render_template, jsonify, request, current_app, Response

leaderboard_bp = Blueprint('leaderboard', __name__)


@leaderboard_bp.route('/')
def leaderboard_page() -> str:
    """
    Render the global leaderboard page.

    Returns:
        Rendered HTML template for the leaderboard.
    """
    return render_template('leaderboard.html')


@leaderboard_bp.route('/data')
def get_leaderboard() -> Response:
    """
    Get sorted leaderboard data as JSON.

    Query Parameters:
        limit (int): Max number of entries (default 50)
        saga (str): Filter by 'voter' or 'officer' scores

    Returns:
        JSON response with the top scores.
    """
    limit = request.args.get('limit', 50, type=int)
    saga = request.args.get('saga', None)
    scores = current_app.firestore.get_top_scores(limit=limit, saga_filter=saga)
    return jsonify({'scores': scores, 'total': len(scores)})


@leaderboard_bp.route('/submit', methods=['POST'])
def submit_score() -> Union[Response, Tuple[Response, int]]:
    """
    Submit a score to the leaderboard with player demographic details.

    Expected JSON body:
        player_name (str): Player's display name
        email (str): Unique identifier
        age (int): 18+ for citizenship verification
        total_score (int): Aggregated score
        voter_score (int): Score from voter saga
        officer_score (int): Score from officer saga
        levels_completed (int): Count of levels finished
        saga_type (str): 'voter', 'officer', or 'both'

    Returns:
        JSON response indicating success.
    """
    data: Optional[Dict[str, Any]] = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    player_name = data.get('player_name', '').strip()
    if not player_name:
        return jsonify({'error': 'Player name is required'}), 400

    email = data.get('email', '').strip()
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    age = data.get('age', 0)
    if not isinstance(age, int) or age < 18 or age > 120:
        return jsonify({'error': 'Valid citizenship age (18+) is required'}), 400

    total_score = data.get('total_score', 0)
    voter_score = data.get('voter_score', 0)
    officer_score = data.get('officer_score', 0)
    levels_completed = data.get('levels_completed', 0)
    saga_type = data.get('saga_type', 'both')

    entry = current_app.firestore.save_score(
        player_name=player_name,
        total_score=total_score,
        levels_completed=levels_completed,
        saga_type=saga_type,
        age=age,
        email=email,
        voter_score=voter_score,
        officer_score=officer_score,
    )

    current_app.cloud_logger.log_score_submitted(player_name, total_score, levels_completed)

    return jsonify({'success': True, 'entry': entry}), 201
