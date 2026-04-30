"""Pytest fixtures for LOKTANTRA tests."""
import pytest
from app import create_app


@pytest.fixture
def app():
    """Create test Flask app."""
    app = create_app('testing')
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_submission_l1():
    """Sample Level 1 submission."""
    return {
        'legitimate': ['v1', 'v2', 'v3', 'v4', 'v5'],
        'ghosts': ['v6', 'v7'],
        'time_seconds': 45,
        'hints_used': 0,
        'player_id': 'test_player',
    }


@pytest.fixture
def sample_submission_l2():
    """Sample Level 2 submission."""
    return {
        'classifications': {
            'n1': True, 'n2': False, 'n3': True, 'n4': False,
            'n5': True, 'n6': False, 'n7': True, 'n8': False,
        },
        'time_seconds': 60,
        'hints_used': 0,
        'player_id': 'test_player',
    }


@pytest.fixture
def sample_submission_l5():
    """Sample Level 5 submission."""
    return {
        'decisions': {'c1': 'accept', 'c2': 'reject', 'c3': 'reject', 'c4': 'reject'},
        'time_seconds': 80,
        'hints_used': 1,
        'player_id': 'test_player',
    }
