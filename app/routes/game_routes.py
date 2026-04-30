"""Game Routes — Level endpoints and submission handling."""
from typing import Any, Dict, Tuple, Union, Optional
from flask import Blueprint, render_template, jsonify, request, current_app, Response
from app.game_engine.levels import get_level, get_all_levels
from app.game_engine.level_data import get_level_data
from app.game_engine.validator import LevelValidator
from app.services.scoring_engine import ScoringEngine

game_bp = Blueprint('game', __name__)


@game_bp.route('/')
def game_shell() -> str:
    """Main game page."""
    levels = get_all_levels()
    return render_template('game.html', levels=levels)


@game_bp.route('/level/<int:level_id>')
def get_level_info(level_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    Get level metadata and data for rendering.

    Args:
        level_id: The ID of the level to retrieve.

    Returns:
        JSON response with level metadata and data.
    """
    level_meta = get_level(level_id)
    if not level_meta:
        return jsonify({'error': 'Level not found'}), 404

    level_data = get_level_data(level_id)
    if not level_data:
        return jsonify({'error': 'Level data not found'}), 404

    # Log level started
    player_id = request.args.get('player_id', 'anonymous')
    current_app.cloud_logger.log_level_started(player_id, level_id)

    return jsonify({
        'meta': level_meta,
        'data': level_data,
    })


@game_bp.route('/level/<int:level_id>/submit', methods=['POST'])
def submit_level(level_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    Submit answers for a level and receive score.

    Args:
        level_id: The ID of the level being submitted.

    Returns:
        JSON response with validation results and score.
    """
    level_data = get_level_data(level_id)
    if not level_data:
        return jsonify({'error': 'Level not found'}), 404

    submission: Optional[Dict[str, Any]] = request.get_json()
    if not submission:
        return jsonify({'error': 'No submission data provided'}), 400

    # Validate answers using the engine
    validation = LevelValidator.validate(level_id, submission, level_data)

    # Calculate score
    time_taken = submission.get('time_seconds', 120)
    hints_used = submission.get('hints_used', 0)
    level_meta = get_level(level_id)
    max_time = level_meta.get('max_time', 120) if level_meta else 120

    score_result = ScoringEngine.calculate_level_score(
        accuracy_pct=validation['accuracy'],
        time_seconds=time_taken,
        hints_used=hints_used,
        max_time=max_time,
    )

    # Log level completed
    player_id = submission.get('player_id', 'anonymous')
    current_app.cloud_logger.log_level_completed(
        player_id=player_id,
        level_id=level_id,
        score=score_result['score'],
        duration_seconds=time_taken,
        stars=score_result['stars'],
    )

    return jsonify({
        'validation': validation,
        'score': score_result,
        'level_id': level_id,
    })
