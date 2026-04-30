"""
Level Validator — Answer validation logic for all 8 levels.
"""
import math
from typing import Dict, Any


class LevelValidator:  # pylint: disable=too-few-public-methods
    """Validates player answers for each level type."""

    @staticmethod
    def validate(
        level_id: int,
        submission: Dict[str, Any],
        level_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate a level submission against reference data.

        Args:
            level_id: Level number (1-8).
            submission: Player's submitted answers (dict).
            level_data: The level's reference data.

        Returns:
            A dictionary with 'correct', 'total', 'accuracy', and 'details'.
        """
        validators = {
            1: LevelValidator._validate_maze,
            2: LevelValidator._validate_classifier,
            3: LevelValidator._validate_sequence,
            4: LevelValidator._validate_precision,
            5: LevelValidator._validate_document_review,
            6: LevelValidator._validate_placement,
            7: LevelValidator._validate_checklist,
            8: LevelValidator._validate_security,
        }
        validator = validators.get(level_id)
        if not validator:
            return {'correct': 0, 'total': 1, 'accuracy': 0.0, 'details': 'Invalid level ID'}

        # Ensure submission and level_data are valid dictionaries
        if not isinstance(submission, dict) or not isinstance(level_data, dict):
            return {'correct': 0, 'total': 1, 'accuracy': 0.0, 'details': 'Invalid data format'}

        return validator(submission, level_data)

    @staticmethod
    def _validate_maze(submission: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """L1: Validate voter identification — legitimate vs ghost."""
        identified_legit = set(submission.get('legitimate', []))
        identified_ghosts = set(submission.get('ghosts', []))
        correct_legit = set(data.get('correct_legitimate', []))
        correct_ghosts = set(data.get('correct_ghosts', []))

        legit_correct = len(identified_legit & correct_legit)
        ghost_correct = len(identified_ghosts & correct_ghosts)
        legit_wrong = len(identified_legit - correct_legit)
        ghost_wrong = len(identified_ghosts - correct_ghosts)

        total = len(correct_legit) + len(correct_ghosts)
        correct = legit_correct + ghost_correct
        penalty = legit_wrong + ghost_wrong
        final = max(0, correct - penalty)

        return {
            'correct': final, 'total': total,
            'accuracy': final / total if total > 0 else 0.0,
            'details': {
                'legitimate_found': legit_correct,
                'ghosts_found': ghost_correct,
                'false_positives': legit_wrong + ghost_wrong,
            }
        }

    @staticmethod
    def _validate_classifier(submission: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """L2: Validate deepfake vs real classification."""
        answers = submission.get('classifications', {})
        news_items = {item['id']: item['is_real'] for item in data.get('news_items', [])}
        total = len(news_items)
        correct = 0
        details = []
        for nid, is_real in news_items.items():
            player_answer = answers.get(nid)
            is_correct = player_answer == is_real
            if is_correct:
                correct += 1
            details.append({'id': nid, 'correct': is_correct})

        return {
            'correct': correct, 'total': total,
            'accuracy': correct / total if total > 0 else 0.0,
            'details': details,
        }

    @staticmethod
    def _validate_sequence(submission: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """L3: Validate EVM voting sequence."""
        player_seq = submission.get('sequence', [])
        correct_seq = data.get('correct_sequence', [])
        total = len(correct_seq)
        correct = 0
        for i, step in enumerate(correct_seq):
            if i < len(player_seq) and player_seq[i] == step:
                correct += 1
            else:
                break  # Sequence must be in order

        return {
            'correct': correct, 'total': total,
            'accuracy': correct / total if total > 0 else 0.0,
            'details': {'steps_correct': correct, 'total_steps': total},
        }

    @staticmethod
    def _validate_precision(submission: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """L4: Validate ink application."""
        finger = submission.get('finger', '')
        position = submission.get('position', '')
        correct_finger = finger == data.get('correct_finger', '')
        correct_position = position == data.get('correct_position', '')
        correct = (1 if correct_finger else 0) + (1 if correct_position else 0)

        return {
            'correct': correct, 'total': 2,
            'accuracy': correct / 2,
            'details': {'correct_finger': correct_finger, 'correct_position': correct_position},
        }

    @staticmethod
    def _validate_document_review(
        submission: Dict[str, Any], data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """L5: Validate candidate affidavit decisions."""
        decisions = submission.get('decisions', {})
        candidates = data.get('candidates', [])
        total = len(candidates)
        correct = 0
        details = []
        for c in candidates:
            player_verdict = decisions.get(c['id'])
            is_correct = player_verdict == c['verdict']
            if is_correct:
                correct += 1
            details.append({'id': c['id'], 'correct': is_correct, 'expected': c['verdict']})

        return {
            'correct': correct, 'total': total,
            'accuracy': correct / total if total > 0 else 0.0,
            'details': details,
        }

    @staticmethod
    def _validate_placement(submission: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """L6: Validate booth placement — all villages within 2km."""
        booths = submission.get('booths', [])
        villages = data.get('villages', [])
        cell_km = data.get('cell_km', 1)
        radius = data.get('radius_km', 2)
        max_booths = data.get('max_booths', 4)

        if len(booths) > max_booths:
            return {'correct': 0, 'total': len(villages), 'accuracy': 0.0,
                    'details': 'Too many booths placed'}

        covered = 0
        uncovered_villages = []
        for v in villages:
            is_covered = False
            for b in booths:
                # Use Euclidean distance for simplicity in this grid-based simulation
                dist = math.sqrt((v['x'] - b['x'])**2 + (v['y'] - b['y'])**2) * cell_km
                if dist <= radius:
                    is_covered = True
                    break
            if is_covered:
                covered += 1
            else:
                uncovered_villages.append(v['name'])

        total = len(villages)
        return {
            'correct': covered, 'total': total,
            'accuracy': covered / total if total > 0 else 0.0,
            'details': {'covered': covered, 'uncovered': uncovered_villages},
        }

    @staticmethod
    def _validate_checklist(submission: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """L7: Validate mock poll checklist order."""
        player_order = submission.get('order', [])
        correct_steps = data.get('steps', [])
        correct_order = [s['action'] for s in sorted(correct_steps, key=lambda x: x['order'])]

        total = len(correct_order)
        correct = 0
        for i, action in enumerate(correct_order):
            if i < len(player_order) and player_order[i] == action:
                correct += 1
            else:
                break

        signatures = submission.get('signatures_collected', False)
        if signatures and correct == total:
            pass  # Full credit
        elif correct == total:
            correct -= 1  # Penalty for missing signatures

        return {
            'correct': correct, 'total': total,
            'accuracy': correct / total if total > 0 else 0.0,
            'details': {'steps_correct': correct, 'signatures': signatures},
        }

    @staticmethod
    def _validate_security(submission: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """L8: Validate seal sequence and custody chain."""
        seal_order = submission.get('seal_order', [])
        correct_order = data.get('correct_seal_order', [])
        custody_done = submission.get('custody_steps_completed', [])
        total_custody = len(data.get('custody_steps', []))

        # Seal ordering
        seal_correct = seal_order == correct_order
        seal_score = 1 if seal_correct else 0

        # Custody steps
        custody_score = len(set(custody_done))

        total = 1 + total_custody
        correct = seal_score + custody_score

        return {
            'correct': correct, 'total': total,
            'accuracy': correct / total if total > 0 else 0.0,
            'details': {'seals_correct': seal_correct, 'custody_steps': custody_score},
        }
