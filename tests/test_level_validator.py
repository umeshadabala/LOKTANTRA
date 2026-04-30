"""Tests for the Level Validator."""
import pytest
from app.game_engine.validator import LevelValidator
from app.game_engine.level_data import get_level_data


class TestLevel1Validator:
    """Test voter identification validation."""

    def test_perfect_identification(self):
        data = get_level_data(1)
        submission = {'legitimate': ['v1', 'v2', 'v3', 'v4', 'v5'], 'ghosts': ['v6', 'v7']}
        result = LevelValidator.validate(1, submission, data)
        assert result['accuracy'] == 1.0
        assert result['correct'] == 7

    def test_all_wrong(self):
        data = get_level_data(1)
        submission = {'legitimate': ['v6', 'v7'], 'ghosts': ['v1', 'v2']}
        result = LevelValidator.validate(1, submission, data)
        assert result['accuracy'] == 0.0

    def test_partial_correct(self):
        data = get_level_data(1)
        submission = {'legitimate': ['v1', 'v2', 'v3'], 'ghosts': ['v6']}
        result = LevelValidator.validate(1, submission, data)
        assert result['correct'] == 4
        assert result['total'] == 7

    def test_empty_submission(self):
        data = get_level_data(1)
        submission = {'legitimate': [], 'ghosts': []}
        result = LevelValidator.validate(1, submission, data)
        assert result['correct'] == 0


class TestLevel2Validator:
    """Test deepfake classifier validation."""

    def test_all_correct(self):
        data = get_level_data(2)
        classifications = {item['id']: item['is_real'] for item in data['news_items']}
        result = LevelValidator.validate(2, {'classifications': classifications}, data)
        assert result['accuracy'] == 1.0

    def test_all_wrong(self):
        data = get_level_data(2)
        classifications = {item['id']: not item['is_real'] for item in data['news_items']}
        result = LevelValidator.validate(2, {'classifications': classifications}, data)
        assert result['accuracy'] == 0.0

    def test_empty_classifications(self):
        data = get_level_data(2)
        result = LevelValidator.validate(2, {'classifications': {}}, data)
        assert result['correct'] == 0


class TestLevel4Validator:
    """Test ink application validation."""

    def test_correct_finger_and_position(self):
        data = get_level_data(4)
        result = LevelValidator.validate(4, {'finger': 'left_index', 'position': 'nail'}, data)
        assert result['accuracy'] == 1.0

    def test_wrong_finger(self):
        data = get_level_data(4)
        result = LevelValidator.validate(4, {'finger': 'right_index', 'position': 'nail'}, data)
        assert result['accuracy'] == 0.5

    def test_wrong_position(self):
        data = get_level_data(4)
        result = LevelValidator.validate(4, {'finger': 'left_index', 'position': 'knuckle'}, data)
        assert result['accuracy'] == 0.5

    def test_both_wrong(self):
        data = get_level_data(4)
        result = LevelValidator.validate(4, {'finger': 'right_thumb', 'position': 'palm'}, data)
        assert result['accuracy'] == 0.0


class TestLevel5Validator:
    """Test candidate scrutiny validation."""

    def test_all_correct(self):
        data = get_level_data(5)
        decisions = {'c1': 'accept', 'c2': 'reject', 'c3': 'reject', 'c4': 'reject'}
        result = LevelValidator.validate(5, {'decisions': decisions}, data)
        assert result['accuracy'] == 1.0

    def test_accept_underage(self):
        data = get_level_data(5)
        decisions = {'c1': 'accept', 'c2': 'accept', 'c3': 'reject', 'c4': 'reject'}
        result = LevelValidator.validate(5, {'decisions': decisions}, data)
        assert result['correct'] == 3  # c2 should be rejected


class TestLevel6Validator:
    """Test booth placement validation."""

    def test_optimal_placement(self):
        data = get_level_data(6)
        booths = [{'x': 2, 'y': 1}, {'x': 5, 'y': 3}, {'x': 1, 'y': 6}, {'x': 7, 'y': 6}]
        result = LevelValidator.validate(6, {'booths': booths}, data)
        assert result['accuracy'] == 1.0

    def test_too_many_booths(self):
        data = get_level_data(6)
        booths = [{'x': i, 'y': i} for i in range(6)]
        result = LevelValidator.validate(6, {'booths': booths}, data)
        assert result['accuracy'] == 0.0

    def test_no_booths(self):
        data = get_level_data(6)
        result = LevelValidator.validate(6, {'booths': []}, data)
        assert result['correct'] == 0


class TestLevel8Validator:
    """Test seal security validation."""

    def test_correct_seal_order(self):
        data = get_level_data(8)
        submission = {
            'seal_order': ['result_section', 'ballot_slot', 'vvpat_chamber'],
            'custody_steps_completed': ['apply_seals', 'record_numbers', 'agent_signatures', 'pack_transport', 'escort_strongroom'],
        }
        result = LevelValidator.validate(8, submission, data)
        assert result['accuracy'] == 1.0

    def test_wrong_seal_order(self):
        data = get_level_data(8)
        submission = {
            'seal_order': ['vvpat_chamber', 'ballot_slot', 'result_section'],
            'custody_steps_completed': [],
        }
        result = LevelValidator.validate(8, submission, data)
        assert result['details']['seals_correct'] is False


class TestInvalidLevel:
    """Test invalid level handling and edge cases."""

    def test_invalid_level_id(self):
        result = LevelValidator.validate(99, {}, {})
        assert result['accuracy'] == 0.0
        assert result['details'] == 'Invalid level ID'

    def test_invalid_submission_type(self):
        # Submission must be a dict
        result = LevelValidator.validate(1, "not a dict", {})  # type: ignore
        assert result['accuracy'] == 0.0
        assert result['details'] == 'Invalid data format'

    def test_invalid_data_type(self):
        # Level data must be a dict
        result = LevelValidator.validate(1, {}, "not a dict")  # type: ignore
        assert result['accuracy'] == 0.0
        assert result['details'] == 'Invalid data format'

    def test_missing_keys_maze(self):
        data = get_level_data(1)
        # Missing 'legitimate' and 'ghosts' keys
        result = LevelValidator.validate(1, {}, data)
        assert result['correct'] == 0
        assert result['total'] == 7

    def test_null_submission(self):
        result = LevelValidator.validate(1, None, {})  # type: ignore
        assert result['accuracy'] == 0.0
        assert result['details'] == 'Invalid data format'


class TestLevel3Validator:
    """Test EVM voting sequence validation."""

    def test_correct_sequence(self):
        data = get_level_data(3)
        submission = {'sequence': data['correct_sequence']}
        result = LevelValidator.validate(3, submission, data)
        assert result['accuracy'] == 1.0

    def test_partial_sequence(self):
        data = get_level_data(3)
        submission = {'sequence': data['correct_sequence'][:2]}
        result = LevelValidator.validate(3, submission, data)
        assert result['correct'] == 2

    def test_wrong_sequence(self):
        data = get_level_data(3)
        submission = {'sequence': list(reversed(data['correct_sequence']))}
        result = LevelValidator.validate(3, submission, data)
        assert result['correct'] == 0


class TestLevel7Validator:
    """Test Mock Poll checklist validation."""

    def test_perfect_checklist(self):
        data = get_level_data(7)
        correct_order = [s['action'] for s in sorted(data['steps'], key=lambda x: x['order'])]
        submission = {'order': correct_order, 'signatures_collected': True}
        result = LevelValidator.validate(7, submission, data)
        assert result['accuracy'] == 1.0

    def test_missing_signatures(self):
        data = get_level_data(7)
        correct_order = [s['action'] for s in sorted(data['steps'], key=lambda x: x['order'])]
        submission = {'order': correct_order, 'signatures_collected': False}
        result = LevelValidator.validate(7, submission, data)
        assert result['correct'] == len(correct_order) - 1

    def test_wrong_order(self):
        data = get_level_data(7)
        correct_order = [s['action'] for s in sorted(data['steps'], key=lambda x: x['order'])]
        submission = {'order': list(reversed(correct_order)), 'signatures_collected': True}
        result = LevelValidator.validate(7, submission, data)
        assert result['correct'] == 0
