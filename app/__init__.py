"""
LOKTANTRA: The Sovereign Saga
Flask Application Factory
"""
import os
from flask import Flask


def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # Load configuration
    from app.config import config_by_name
    env = config_name or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config_by_name.get(env, config_by_name['development']))

    # Initialize services
    _init_services(app)

    # Register blueprints
    _register_blueprints(app)

    # Register error handlers
    _register_error_handlers(app)

    # Template context processors
    @app.context_processor
    def inject_globals():
        return {
            'app_name': 'LOKTANTRA',
            'app_subtitle': 'The Sovereign Saga',
        }

    return app


def _init_services(app):
    """Initialize Google Cloud services with graceful fallbacks."""
    from app.services.firestore_service import FirestoreService
    from app.services.vertex_ai_service import VertexAIService
    from app.services.logging_service import LoggingService

    app.firestore = FirestoreService(app)
    app.vertex_ai = VertexAIService(app)
    app.cloud_logger = LoggingService(app)


def _register_blueprints(app):
    """Register all route blueprints."""
    from app.routes.main_routes import main_bp
    from app.routes.game_routes import game_bp
    from app.routes.leaderboard_routes import leaderboard_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(game_bp, url_prefix='/game')
    app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
    app.register_blueprint(api_bp, url_prefix='/api')


def _register_error_handlers(app):
    """Register custom error handlers."""
    from flask import render_template, jsonify, request

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Resource not found'}), 404
        return render_template('base.html', error_code=404,
                               error_message='Page not found'), 404

    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('base.html', error_code=500,
                               error_message='Internal server error'), 500
