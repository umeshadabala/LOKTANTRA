"""Main Routes — Landing page, health check, about."""
from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page with game overview."""
    from app.game_engine.levels import get_all_levels, PARTIES
    levels = get_all_levels()
    return render_template('index.html', levels=levels, parties=PARTIES)


@main_bp.route('/health')
def health():
    """Health check endpoint for Cloud Run."""
    return jsonify({'status': 'healthy', 'service': 'loktantra'}), 200


@main_bp.route('/about')
def about():
    """About the project."""
    return render_template('index.html', show_about=True)
