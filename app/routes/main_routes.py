"""Main Routes — Landing page, health check, and basic views."""
from typing import Any
from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index() -> str:
    """
    Render the landing page with game overview and party manifestos.

    Returns:
        Rendered HTML template for the index page.
    """
    from app.game_engine.levels import get_all_levels, PARTIES  # pylint: disable=import-outside-toplevel
    levels = get_all_levels()
    return render_template('index.html', levels=levels, parties=PARTIES)


@main_bp.route('/health')
def health() -> Any:
    """
    Health check endpoint for Cloud Run and monitoring services.

    Returns:
        JSON response with health status.
    """
    return jsonify({'status': 'healthy', 'service': 'loktantra'}), 200


@main_bp.route('/about')
def about() -> str:
    """
    Render the about section of the project.

    Returns:
        Rendered HTML template for the about page.
    """
    return render_template('index.html', show_about=True)
