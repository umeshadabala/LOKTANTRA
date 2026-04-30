"""
LOKTANTRA: The Sovereign Saga
Flask Application Factory
"""
import os
from typing import Dict, Optional
from flask import Flask


def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Create and configure the Flask application factory.

    Args:
        config_name: Configuration name (development, production, testing).

    Returns:
        The configured Flask application instance.
    """
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # Load configuration
    from app.config import config_by_name  # pylint: disable=import-outside-toplevel
    env = config_name or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(
        config_by_name.get(env, config_by_name['development'])
    )

    # Initialize services
    _init_services(app)

    # Register blueprints
    _register_blueprints(app)

    # Register error handlers
    _register_error_handlers(app)

    # Template context processors
    @app.context_processor
    def inject_globals() -> Dict[str, str]:
        return {
            'app_name': 'LOKTANTRA',
            'app_subtitle': 'The Sovereign Saga',
        }

    return app


def _init_services(app: Flask) -> None:
    """
    Initialize Google Cloud services with graceful fallbacks.

    Args:
        app: The Flask application instance.
    """
    # pylint: disable=import-outside-toplevel
    from app.services.firestore_service import FirestoreService
    from app.services.vertex_ai_service import VertexAIService
    from app.services.logging_service import LoggingService

    app.firestore = FirestoreService(app)
    app.vertex_ai = VertexAIService(app)
    app.cloud_logger = LoggingService(app)


def _register_blueprints(app: Flask) -> None:
    """
    Register all route blueprints.

    Args:
        app: The Flask application instance.
    """
    # pylint: disable=import-outside-toplevel
    from app.routes.main_routes import main_bp
    from app.routes.game_routes import game_bp
    from app.routes.leaderboard_routes import leaderboard_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(game_bp, url_prefix='/game')
    app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
    app.register_blueprint(api_bp, url_prefix='/api')


def _register_error_handlers(app: Flask) -> None:
    """
    Register custom error handlers.

    Args:
        app: The Flask application instance.
    """
    from flask import render_template, jsonify, request  # pylint: disable=import-outside-toplevel

    @app.errorhandler(404)
    def not_found(_error: Exception) -> tuple:
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Resource not found'}), 404
        return render_template(
            'base.html', error_code=404,
            error_message='Page not found'
        ), 404

    @app.errorhandler(500)
    def internal_error(_error: Exception) -> tuple:
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template(
            'base.html', error_code=500,
            error_message='Internal server error'
        ), 500
