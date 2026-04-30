"""
Leaderboard Routes — Global Civic Leaderboard endpoints.

Provides endpoints for:
- Rendering the leaderboard page.
- Fetching sorted leaderboard data with saga filtering.
- Submitting validated player scores with demographic details.
"""
import logging
from typing import Tuple, Union, Optional
from flask import Blueprint, render_template, jsonify, request, current_app, Response
from app.utils import (
    sanitize_text, validate_email, validate_player_age, validate_score,
    MAX_TOTAL_SCORE,
)

logger = logging.getLogger(__name__)

leaderboard_bp = Blueprint('leaderboard', __name__)

# Valid saga filter values
VALID_SAGA_TYPES = frozenset({'voter', 'officer', 'both'})


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
        limit (int): Max number of entries, default 50, max 100.
        saga (str): Filter by 'voter' or 'officer' scores.

    Returns:
        JSON with 'scores' list and 'total' count.
    """
    limit = min(request.args.get('limit', 50, type=int), 100)
    saga = request.args.get('saga', None)

    # Validate saga filter
    if saga and saga not in VALID_SAGA_TYPES:
        saga = None

    scores = current_app.firestore.get_top_scores(
        limit=limit, saga_filter=saga,
    )
    return jsonify({'scores': scores, 'total': len(scores)})


@leaderboard_bp.route('/submit', methods=['POST'])
def submit_score() -> Union[Response, Tuple[Response, int]]:
    """
    Submit a score to the leaderboard with player details.

    Expected JSON body:
        player_name (str): Player's display name (required).
        email (str): Unique identifier (required).
        age (int): Citizenship age, must be 18+ (required).
        total_score (int): Aggregated score across levels.
        voter_score (int): Score from the Voter Saga.
        officer_score (int): Score from the Officer Saga.
        levels_completed (int): Count of levels finished.
        saga_type (str): One of 'voter', 'officer', or 'both'.

    Returns:
        JSON with 'success' flag and saved 'entry'.

    Status Codes:
        201: Score submitted successfully.
        400: Invalid or missing required fields.
    """
    data: Optional[dict] = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validate required fields
    player_name = sanitize_text(data.get('player_name', ''))
    if not player_name:
        return jsonify({'error': 'Player name is required'}), 400

    email = sanitize_text(data.get('email', ''))
    if not validate_email(email):
        return jsonify({'error': 'Valid email is required'}), 400

    age = data.get('age', 0)
    if not validate_player_age(age):
        return jsonify({'error': 'Valid citizenship age (18+) is required'}), 400

    # Validate and clamp scores
    total_score = validate_score(data.get('total_score', 0), MAX_TOTAL_SCORE)
    voter_score = validate_score(data.get('voter_score', 0))
    officer_score = validate_score(data.get('officer_score', 0))
    levels_completed = max(0, min(int(data.get('levels_completed', 0)), 8))

    saga_type = data.get('saga_type', 'both')
    if saga_type not in VALID_SAGA_TYPES:
        saga_type = 'both'

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

    current_app.cloud_logger.log_score_submitted(
        player_name, total_score, levels_completed,
    )
    logger.info(
        "Score submitted: player=%s score=%d levels=%d",
        player_name, total_score, levels_completed,
    )

    return jsonify({'success': True, 'entry': entry}), 201
