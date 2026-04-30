"""
Scoring Engine — Per-level and aggregate scoring logic.
"""
from typing import Dict, Any


class ScoringEngine:
    """Calculates scores for each level and aggregates totals with consistent logic."""

    MAX_SCORE_PER_LEVEL: int = 100
    MAX_LEVELS: int = 8
    TIME_BONUS_THRESHOLD: int = 60  # seconds — under this gets a bonus
    HINT_PENALTY: int = 10

    # Star thresholds (percentage of max)
    STAR_THRESHOLDS: Dict[int, float] = {1: 0.50, 2: 0.75, 3: 0.90}

    @staticmethod
    def calculate_level_score(accuracy_pct: float,
                               time_seconds: int,
                               *,
                               hints_used: int = 0,
                               max_time: int = 120) -> Dict[str, Any]:
        """
        Calculate score for a single level.

        Args:
            accuracy_pct: Float 0.0-1.0 representing answer accuracy.
            time_seconds: Time taken in seconds.
            hints_used: Number of hints used.
            max_time: Maximum allowed time for the level.

        Returns:
            A dictionary with 'score', 'time_bonus', 'hint_penalty', 'stars', and 'breakdown'.
        """
        # Base score is 70% of max
        base = int(accuracy_pct * 70)

        # Time bonus: up to 20 points for being fast
        if time_seconds <= 0:
            time_bonus = 20
        elif time_seconds < ScoringEngine.TIME_BONUS_THRESHOLD:
            ratio = 1.0 - (time_seconds / ScoringEngine.TIME_BONUS_THRESHOLD)
            time_bonus = int(ratio * 20)
        else:
            time_bonus = 0

        # Completion bonus: 10 points for finishing
        completion_bonus = 10 if accuracy_pct > 0 else 0

        # Hint penalty: capped at 30 points
        hint_penalty = min(hints_used * ScoringEngine.HINT_PENALTY, 30)

        raw = base + time_bonus + completion_bonus - hint_penalty
        final = max(0, min(raw, ScoringEngine.MAX_SCORE_PER_LEVEL))

        stars = ScoringEngine.calculate_stars(final)

        return {
            'score': final,
            'base_accuracy': base,
            'time_bonus': time_bonus,
            'completion_bonus': completion_bonus,
            'hint_penalty': hint_penalty,
            'stars': stars,
            'max_score': ScoringEngine.MAX_SCORE_PER_LEVEL,
        }

    @staticmethod
    def calculate_stars(score: int) -> int:
        """
        Calculate star rating from score.

        Args:
            score: The final score achieved.

        Returns:
            Number of stars (0-3).
        """
        pct = score / ScoringEngine.MAX_SCORE_PER_LEVEL
        if pct >= ScoringEngine.STAR_THRESHOLDS[3]:
            return 3
        if pct >= ScoringEngine.STAR_THRESHOLDS[2]:
            return 2
        if pct >= ScoringEngine.STAR_THRESHOLDS[1]:
            return 1
        return 0

    @staticmethod
    def calculate_aggregate(level_scores: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate aggregate score across all completed levels.

        Args:
            level_scores: A dictionary mapping level_id to score dict.

        Returns:
            A dictionary with 'total_score', 'levels_completed', 'average', and 'star_total'.
        """
        if not level_scores:
            return {
                'total_score': 0, 'levels_completed': 0,
                'average_score': 0.0, 'total_stars': 0,
                'max_possible': ScoringEngine.MAX_SCORE_PER_LEVEL * ScoringEngine.MAX_LEVELS,
                'completion_pct': 0.0,
            }

        total = sum(s.get('score', 0) for s in level_scores.values())
        count = len(level_scores)
        total_stars = sum(s.get('stars', 0) for s in level_scores.values())
        max_possible = ScoringEngine.MAX_SCORE_PER_LEVEL * ScoringEngine.MAX_LEVELS

        return {
            'total_score': total,
            'levels_completed': count,
            'average_score': round(total / count, 1) if count else 0.0,
            'total_stars': total_stars,
            'max_possible': max_possible,
            'completion_pct': round((count / ScoringEngine.MAX_LEVELS) * 100, 1),
        }
