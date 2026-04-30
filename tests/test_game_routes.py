"""Tests for game routes."""
import json
import pytest


class TestHealthCheck:
    def test_health_returns_200(self, client):
        resp = client.get('/health')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'healthy'


class TestMainRoutes:
    def test_index_returns_200(self, client):
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'LOKTANTRA' in resp.data

    def test_game_page_returns_200(self, client):
        resp = client.get('/game/')
        assert resp.status_code == 200

    def test_leaderboard_page_returns_200(self, client):
        resp = client.get('/leaderboard/')
        assert resp.status_code == 200


class TestGameRoutes:
    def test_get_level_1(self, client):
        resp = client.get('/game/level/1')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['meta']['id'] == 1
        assert 'voters' in data['data']

    def test_get_level_invalid(self, client):
        resp = client.get('/game/level/99')
        assert resp.status_code == 404

    def test_submit_level_1(self, client, sample_submission_l1):
        resp = client.post('/game/level/1/submit',
                           data=json.dumps(sample_submission_l1),
                           content_type='application/json')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'score' in data
        assert 'validation' in data
        assert data['score']['score'] > 0

    def test_submit_level_5(self, client, sample_submission_l5):
        resp = client.post('/game/level/5/submit',
                           data=json.dumps(sample_submission_l5),
                           content_type='application/json')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['validation']['accuracy'] == 1.0

    def test_submit_no_body(self, client):
        resp = client.post('/game/level/1/submit', content_type='application/json')
        assert resp.status_code == 400


class TestAPIRoutes:
    def test_explain_level_1(self, client):
        resp = client.post('/api/explain',
                           data=json.dumps({'level_id': 1}),
                           content_type='application/json')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'explanation' in data
        assert data['explanation']['title']

    def test_explain_invalid_level(self, client):
        resp = client.post('/api/explain',
                           data=json.dumps({'level_id': 99}),
                           content_type='application/json')
        assert resp.status_code == 400

    def test_explain_no_body(self, client):
        resp = client.post('/api/explain', content_type='application/json')
        assert resp.status_code == 400


class TestLeaderboardRoutes:
    def test_get_leaderboard_data(self, client):
        resp = client.get('/leaderboard/data')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'scores' in data

    def test_submit_score(self, client):
        resp = client.post('/leaderboard/submit',
                           data=json.dumps({
                               'player_name': 'TestPlayer',
                               'age': 18,
                               'email': 'test@example.com',
                               'total_score': 500,
                               'levels_completed': 5,
                           }),
                           content_type='application/json')
        assert resp.status_code == 201

    def test_submit_score_no_name(self, client):
        resp = client.post('/leaderboard/submit',
                           data=json.dumps({'total_score': 500, 'age': 18, 'email': 'a@b.com'}),
                           content_type='application/json')
        assert resp.status_code == 400

    def test_submit_score_no_email(self, client):
        resp = client.post('/leaderboard/submit',
                           data=json.dumps({'player_name': 'Test', 'total_score': 500, 'age': 18}),
                           content_type='application/json')
        assert resp.status_code == 400
