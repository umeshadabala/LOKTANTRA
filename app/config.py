"""
LOKTANTRA Configuration Management
Supports development (local) and production (Cloud Run) environments.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:  # pylint: disable=too-few-public-methods
    """Base configuration."""
    SECRET_KEY = os.getenv(
        'SECRET_KEY', 'loktantra-dev-secret-key-change-in-prod'
    )

    # Google Cloud
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', '')
    GCP_LOCATION = os.getenv('GCP_LOCATION', 'us-central1')

    # Firestore
    FIRESTORE_COLLECTION_LEADERBOARD = os.getenv(
        'FIRESTORE_COLLECTION_LEADERBOARD', 'leaderboard'
    )
    FIRESTORE_COLLECTION_PROGRESS = os.getenv(
        'FIRESTORE_COLLECTION_PROGRESS', 'player_progress'
    )

    # Vertex AI
    VERTEX_AI_MODEL = os.getenv('VERTEX_AI_MODEL', 'gemini-1.5-pro')
    VERTEX_AI_LOCATION = os.getenv('VERTEX_AI_LOCATION', 'us-central1')

    # Feature Flags
    ENABLE_FIRESTORE = (
        os.getenv('ENABLE_FIRESTORE', 'false').lower() == 'true'
    )
    ENABLE_VERTEX_AI = (
        os.getenv('ENABLE_VERTEX_AI', 'false').lower() == 'true'
    )
    ENABLE_CLOUD_LOGGING = (
        os.getenv('ENABLE_CLOUD_LOGGING', 'false').lower() == 'true'
    )

    # Game Settings
    MAX_LEVELS = 8
    MAX_SCORE_PER_LEVEL = 100
    MAX_TOTAL_SCORE = 800
    LEADERBOARD_TOP_N = 50


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """Production configuration for Cloud Run."""
    DEBUG = False
    TESTING = False
    ENABLE_FIRESTORE = bool(os.getenv('GCP_PROJECT_ID', ''))
    ENABLE_VERTEX_AI = bool(os.getenv('GCP_PROJECT_ID', ''))
    ENABLE_CLOUD_LOGGING = bool(os.getenv('GCP_PROJECT_ID', ''))


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    ENABLE_FIRESTORE = False
    ENABLE_VERTEX_AI = False
    ENABLE_CLOUD_LOGGING = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
