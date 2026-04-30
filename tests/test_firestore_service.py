"""Tests for Firestore Service (in-memory fallback mode) — Enhanced deduplication & filtering."""
import pytest


class TestFirestoreInMemory:
    """Test Firestore service with in-memory fallback."""

    def test_save_and_get_score(self, app):
        entry = app.firestore.save_score('Alice', 750, 8, email='alice@test.com')
        assert entry['player_name'] == 'Alice'
        assert entry['total_score'] == 750

        scores = app.firestore.get_top_scores(limit=10)
        assert len(scores) >= 1
        assert any(s['player_name'] == 'Alice' for s in scores)

    def test_deduplication_by_email(self, app):
        """Test that same email updates score rather than creating new entry."""
        app.firestore.save_score('Bob', 100, 1, email='bob@test.com')
        app.firestore.save_score('Bob', 500, 4, email='bob@test.com')
        
        scores = app.firestore.get_top_scores(limit=10)
        # Check that Bob only appears once
        bob_entries = [s for s in scores if s['email'] == 'bob@test.com']
        assert len(bob_entries) == 1
        assert bob_entries[0]['total_score'] == 500

    def test_saga_specific_filtering(self, app):
        """Test that Voter/Officer leaderboards are segregated."""
        # Voter only player
        app.firestore.save_score('VoterOnly', 300, 3, email='v@test.com', voter_score=300, saga_type='voter')
        # Officer only player
        app.firestore.save_score('OfficerOnly', 400, 4, email='o@test.com', officer_score=400, saga_type='officer')
        # Both player
        app.firestore.save_score('BothPlayer', 700, 7, email='b@test.com', voter_score=350, officer_score=350, saga_type='both')

        # Voter leaderboard should show VoterOnly and BothPlayer (sorted by voter_score)
        voter_scores = app.firestore.get_top_scores(saga_filter='voter')
        assert len(voter_scores) == 2
        assert voter_scores[0]['player_name'] == 'BothPlayer' # 350 > 300
        assert not any(s['player_name'] == 'OfficerOnly' for s in voter_scores)

        # Officer leaderboard
        officer_scores = app.firestore.get_top_scores(saga_filter='officer')
        assert len(officer_scores) == 2
        assert officer_scores[0]['player_name'] == 'OfficerOnly' # 400 > 350
        assert not any(s['player_name'] == 'VoterOnly' for s in officer_scores)

    def test_scores_sorted_descending(self, app):
        app.firestore.save_score('Low', 100, 2, email='low@t.com')
        app.firestore.save_score('High', 800, 8, email='high@t.com')
        app.firestore.save_score('Mid', 500, 5, email='mid@t.com')

        scores = app.firestore.get_top_scores(limit=10)
        # Ensure Bob/Alice/etc from other tests don't break the sort check
        for i in range(len(scores) - 1):
            assert scores[i]['total_score'] >= scores[i + 1]['total_score']

    def test_save_and_get_progress(self, app):
        progress = {'levels': {1: {'score': 90}}, 'current_level': 2, 'total_score': 90}
        app.firestore.save_progress('session123', progress)

        loaded = app.firestore.get_progress('session123')
        assert loaded is not None
        assert loaded['current_level'] == 2

    def test_get_nonexistent_progress(self, app):
        result = app.firestore.get_progress('nonexistent')
        assert result is None

    def test_clear_progress(self, app):
        app.firestore.save_progress('sess_clear', {'current_level': 1})
        app.firestore.clear_progress('sess_clear')
        assert app.firestore.get_progress('sess_clear') is None
