"""
Game Routes — Level endpoints and submission handling.

Provides endpoints for:
- Rendering the main game page with all level metadata.
- Fetching individual level data for gameplay.
- Validating and scoring level submissions.
"""
import logging
from typing import Tuple, Union, Optional
from flask import Blueprint, render_template, jsonify, request, current_app, Response
from app.game_engine.levels import get_level, get_all_levels
from app.game_engine.level_data import get_level_data
from app.game_engine.validator import LevelValidator
from app.services.scoring_engine import ScoringEngine
from app.utils import sanitize_text, validate_level_id

logger = logging.getLogger(__name__)

game_bp = Blueprint('game', __name__)


@game_bp.route('/')
def game_shell() -> str:
    """
    Render the main game page with level selection grid.

    Returns:
        Rendered game.html template with all level metadata.
    """
    levels = get_all_levels()
    return render_template('game.html', levels=levels)


@game_bp.route('/level/<int:level_id>')
def get_level_info(level_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    Fetch level metadata and gameplay data for rendering.

    Args:
        level_id: The ID of the level to retrieve (1-8).

    Returns:
        JSON with 'meta' (level metadata) and 'data' (gameplay content).

    Status Codes:
        200: Level data retrieved successfully.
        404: Level not found.
    """
    if not validate_level_id(level_id):
        return jsonify({'error': 'Invalid level ID'}), 404

    level_meta = get_level(level_id)
    if not level_meta:
        return jsonify({'error': 'Level not found'}), 404

    level_data = get_level_data(level_id)
    if not level_data:
        return jsonify({'error': 'Level data not found'}), 404

    # Audit trail: log level access
    player_id = sanitize_text(
        request.args.get('player_id', 'anonymous'),
    )
    current_app.cloud_logger.log_level_started(player_id, level_id)
    logger.info("Level %d started by player: %s", level_id, player_id)

    return jsonify({
        'meta': level_meta,
        'data': level_data,
    })


@game_bp.route('/level/<int:level_id>/submit', methods=['POST'])
def submit_level(level_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    Submit answers for a level and receive a calculated score.

    Args:
        level_id: The ID of the level being submitted (1-8).

    Expected JSON body:
        time_seconds (int): Time taken to complete the level.
        hints_used (int): Number of hints consumed.
        player_id (str): Unique player identifier.
        (additional level-specific answer fields)

    Returns:
        JSON with 'validation' results, 'score' breakdown, and 'level_id'.

    Status Codes:
        200: Submission scored successfully.
        400: Missing or invalid submission data.
        404: Level not found.
    """
    if not validate_level_id(level_id):
        return jsonify({'error': 'Invalid level ID'}), 404

    level_data = get_level_data(level_id)
    if not level_data:
        return jsonify({'error': 'Level not found'}), 404

    submission: Optional[dict] = request.get_json()
    if not submission:
        return jsonify({'error': 'No submission data provided'}), 400

    # Server-side validation of answers
    validation = LevelValidator.validate(level_id, submission, level_data)

    # Extract timing and hint data with safe defaults
    time_taken = max(0, int(submission.get('time_seconds', 120)))
    hints_used = max(0, min(int(submission.get('hints_used', 0)), 3))
    level_meta = get_level(level_id)
    max_time = level_meta.get('max_time', 120) if level_meta else 120

    # Calculate score using the scoring engine
    score_result = ScoringEngine.calculate_level_score(
        accuracy_pct=validation['accuracy'],
        time_seconds=time_taken,
        hints_used=hints_used,
        max_time=max_time,
    )

    # Audit trail: log level completion
    player_id = sanitize_text(
        submission.get('player_id', 'anonymous'),
    )
    current_app.cloud_logger.log_level_completed(
        player_id=player_id,
        level_id=level_id,
        score=score_result['score'],
        duration_seconds=time_taken,
        stars=score_result['stars'],
    )
    logger.info(
        "Level %d submitted: player=%s score=%d stars=%d",
        level_id, player_id, score_result['score'], score_result['stars'],
    )

    return jsonify({
        'validation': validation,
        'score': score_result,
        'level_id': level_id,
    })
