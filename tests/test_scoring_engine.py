"""Tests for the Scoring Engine."""
import pytest
from app.services.scoring_engine import ScoringEngine


class TestScoreCalculation:
    """Test per-level score calculation."""

    def test_perfect_score_fast(self):
        result = ScoringEngine.calculate_level_score(1.0, 10, hints_used=0)
        # 70 (accuracy) + 16 (time bonus) + 10 (completion) = 96
        assert result['score'] == 96
        assert result['stars'] == 3

    def test_perfect_accuracy_slow(self):
        result = ScoringEngine.calculate_level_score(1.0, 120, hints_used=0)
        assert result['base_accuracy'] == 70
        assert result['time_bonus'] == 0
        assert result['score'] == 80  # 70 + 0 + 10

    def test_half_accuracy(self):
        result = ScoringEngine.calculate_level_score(0.5, 30, hints_used=0)
        assert result['base_accuracy'] == 35

    def test_zero_accuracy(self):
        result = ScoringEngine.calculate_level_score(0.0, 10, hints_used=0)
        # 0 accuracy + time_bonus but no completion = time_bonus only
        assert result['completion_bonus'] == 0
        assert result['base_accuracy'] == 0
        assert result['stars'] == 0

    def test_hint_penalty(self):
        no_hints = ScoringEngine.calculate_level_score(1.0, 30, hints_used=0)
        one_hint = ScoringEngine.calculate_level_score(1.0, 30, hints_used=1)
        assert no_hints['score'] - one_hint['score'] == 10

    def test_max_hint_penalty_capped(self):
        result = ScoringEngine.calculate_level_score(1.0, 10, hints_used=5)
        assert result['hint_penalty'] == 30  # Capped at 30

    def test_score_never_negative(self):
        result = ScoringEngine.calculate_level_score(0.1, 120, hints_used=3)
        assert result['score'] >= 0

    def test_score_never_exceeds_max(self):
        result = ScoringEngine.calculate_level_score(1.0, 0, hints_used=0)
        assert result['score'] <= 100

    def test_time_bonus_at_boundary(self):
        result = ScoringEngine.calculate_level_score(1.0, 60, hints_used=0)
        assert result['time_bonus'] == 0  # Exactly at threshold

    def test_negative_time_gives_max_bonus(self):
        result = ScoringEngine.calculate_level_score(1.0, -5, hints_used=0)
        assert result['time_bonus'] == 20

    def test_keyword_only_max_time(self):
        result = ScoringEngine.calculate_level_score(
            1.0, 10, hints_used=0, max_time=180
        )
        assert result['score'] > 0


class TestStarRating:
    """Test star rating calculations."""

    def test_three_stars(self):
        assert ScoringEngine.calculate_stars(90) == 3
        assert ScoringEngine.calculate_stars(95) == 3
        assert ScoringEngine.calculate_stars(100) == 3

    def test_two_stars(self):
        assert ScoringEngine.calculate_stars(75) == 2
        assert ScoringEngine.calculate_stars(89) == 2

    def test_one_star(self):
        assert ScoringEngine.calculate_stars(50) == 1
        assert ScoringEngine.calculate_stars(74) == 1

    def test_zero_stars(self):
        assert ScoringEngine.calculate_stars(0) == 0
        assert ScoringEngine.calculate_stars(49) == 0


class TestAggregate:
    """Test aggregate score calculation."""

    def test_empty_scores(self):
        result = ScoringEngine.calculate_aggregate({})
        assert result['total_score'] == 0
        assert result['levels_completed'] == 0

    def test_single_level(self):
        scores = {1: {'score': 85, 'stars': 2}}
        result = ScoringEngine.calculate_aggregate(scores)
        assert result['total_score'] == 85
        assert result['levels_completed'] == 1
        assert result['completion_pct'] == 12.5

    def test_all_levels_perfect(self):
        scores = {i: {'score': 100, 'stars': 3} for i in range(1, 9)}
        result = ScoringEngine.calculate_aggregate(scores)
        assert result['total_score'] == 800
        assert result['levels_completed'] == 8
        assert result['total_stars'] == 24
        assert result['completion_pct'] == 100.0

    def test_average_calculation(self):
        scores = {1: {'score': 60, 'stars': 1}, 2: {'score': 80, 'stars': 2}}
        result = ScoringEngine.calculate_aggregate(scores)
        assert result['average_score'] == 70.0
