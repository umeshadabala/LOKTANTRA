"""Tests for API Routes (progress & explanation)."""
import json


class TestAPIRoutes:
    def test_explain_valid(self, client):
        resp = client.post('/api/explain',
                           data=json.dumps({'level_id': 1, 'player_id': 'test_user'}),
                           content_type='application/json')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['level_id'] == 1
        assert 'explanation' in data
        assert data['source'] in ['vertex_ai', 'static']

    def test_explain_no_data(self, client):
        resp = client.post('/api/explain', content_type='application/json')
        assert resp.status_code == 400

    def test_explain_invalid_level(self, client):
        resp = client.post('/api/explain',
                           data=json.dumps({'level_id': 99}),
                           content_type='application/json')
        assert resp.status_code == 400

    def test_save_and_get_progress(self, client):
        # Save progress
        save_data = {
            'session_id': 'sess123',
            'levels': {1: {'score': 100}},
            'current_level': 2
        }
        resp = client.post('/api/progress',
                           data=json.dumps(save_data),
                           content_type='application/json')
        assert resp.status_code == 200
        assert json.loads(resp.data)['success'] is True

        # Get progress
        resp2 = client.get('/api/progress/sess123')
        assert resp2.status_code == 200
        data2 = json.loads(resp2.data)
        assert data2['exists'] is True
        assert data2['progress']['current_level'] == 2

    def test_get_progress_not_found(self, client):
        resp = client.get('/api/progress/nonexistent')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['exists'] is False
        assert data['progress'] is None

    def test_save_progress_no_data(self, client):
        resp = client.post('/api/progress', content_type='application/json')
        assert resp.status_code == 400

    def test_save_progress_no_session(self, client):
        resp = client.post('/api/progress',
                           data=json.dumps({'levels': {}}),
                           content_type='application/json')
        assert resp.status_code == 400
