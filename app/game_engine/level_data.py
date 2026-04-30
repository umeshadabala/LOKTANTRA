"""
Level Data — Questions, answers, and interactive content for all 8 levels.
"""
from typing import Dict, Any, Optional

LEVEL_DATA: Dict[int, Dict[str, Any]] = {
    1: {
        'type': 'maze_search',
        'voters': [
            {'id': 'v1', 'name': 'Priya Sharma', 'age': 28, 'voter_id': 'DL/04/123/456789',
             'constituency': 'Chandni Chowk', 'legitimate': True},
            {'id': 'v2', 'name': 'Arjun Patel', 'age': 35, 'voter_id': 'GJ/07/234/567890',
             'constituency': 'Sabarmati', 'legitimate': True},
            {'id': 'v3', 'name': 'Fatima Khan', 'age': 22, 'voter_id': 'UP/11/345/678901',
             'constituency': 'Lucknow Central', 'legitimate': True},
            {'id': 'v4', 'name': 'Ravi Kumar', 'age': 45, 'voter_id': 'KA/02/456/789012',
             'constituency': 'Bengaluru South', 'legitimate': True},
            {'id': 'v5', 'name': 'Ananya Das', 'age': 19, 'voter_id': 'WB/09/567/890123',
             'constituency': 'Kolkata North', 'legitimate': True},
            {'id': 'v6', 'name': 'Ghost Voter A', 'age': 150, 'voter_id': 'XX/00/000/000001',
             'constituency': 'Nowhere', 'legitimate': False},
            {'id': 'v7', 'name': 'Duplicate Entry', 'age': 28, 'voter_id': 'DL/04/123/456789',
             'constituency': 'Chandni Chowk', 'legitimate': False},
        ],
        'correct_legitimate': ['v1', 'v2', 'v3', 'v4', 'v5'],
        'correct_ghosts': ['v6', 'v7'],
        'maze_size': {'rows': 5, 'cols': 5},
    },
    2: {
        'type': 'classifier',
        'news_items': [
            {'id': 'n1', 'headline': 'ECI announces polling dates for Phase 3 in 5 states',
             'source': 'Press Information Bureau', 'is_real': True,
             'explanation': 'Official government press release with verifiable dates.'},
            {'id': 'n2', 'headline': 'BREAKING: Blue Lotus Party leader caught in secret deal',
             'source': 'Unknown WhatsApp Forward', 'is_real': False,
             'explanation': 'No credited source. AI-generated audio with artifacts.'},
            {'id': 'n3', 'headline': 'Supreme Court upholds EVM integrity after independent audit',
             'source': 'The Constitutional Gazette', 'is_real': True,
             'explanation': 'Verifiable court ruling from public records.'},
            {'id': 'n4', 'headline': 'Golden Gear Party to give FREE laptops to all voters',
             'source': 'Social Media Viral Post', 'is_real': False,
             'explanation': 'Vote-buying promise violates Model Code.'},
            {'id': 'n5', 'headline': 'Voter turnout in Phase 1 reaches 67.4% — ECI official data',
             'source': 'Election Commission Website', 'is_real': True,
             'explanation': 'Official statistics from eci.gov.in with matching data.'},
            {'id': 'n6', 'headline': 'EVM machines hacked! Video shows manipulation in real-time',
             'source': 'Anonymous YouTube Channel', 'is_real': False,
             'explanation': 'Video uses edited footage. EVMs are standalone devices.'},
            {'id': 'n7', 'headline': 'New voter registration drive targets 18-19 age group',
             'source': 'National Voters Service Portal', 'is_real': True,
             'explanation': 'Official NVSP initiative aligned with Article 326.'},
            {'id': 'n8', 'headline': 'Rival candidate seen bribing officials at counting center',
             'source': 'Deepfake Video on Telegram', 'is_real': False,
             'explanation': 'AI-generated video with face-swap artifacts.'},
        ],
    },
    3: {
        'type': 'sequence',
        'steps': [
            {'step': 1, 'action': 'enter_booth', 'label': 'Enter the Voting Booth',
             'description': 'Step behind the curtain into the private voting compartment.'},
            {'step': 2, 'action': 'view_ballot', 'label': 'View the Ballot Unit',
             'description': 'See the candidate names, party symbols, and blue buttons.'},
            {'step': 3, 'action': 'press_button', 'label': 'Press the Blue Button',
             'description': 'Press the blue button next to your chosen candidate.'},
            {'step': 4, 'action': 'verify_vvpat', 'label': 'Verify VVPAT Slip',
             'description': 'Watch the printed slip showing your candidate for 7 seconds.'},
            {'step': 5, 'action': 'hear_beep', 'label': 'Confirm the Beep',
             'description': 'A long beep from the Control Unit confirms your vote.'},
            {'step': 6, 'action': 'exit_booth', 'label': 'Exit the Booth',
             'description': 'Your vote is cast. Exit the booth and proceed to the ink station.'},
        ],
        'candidates': [
            {'name': 'Kavita Menon', 'party': 'blue_lotus', 'position': 1},
            {'name': 'Rajesh Tiwari', 'party': 'golden_gear', 'position': 2},
            {'name': 'Sunita Devi', 'party': 'rising_sun', 'position': 3},
            {'name': 'Amir Hassan', 'party': 'eternal_flame', 'position': 4},
        ],
        'correct_sequence': ['enter_booth', 'view_ballot', 'press_button', 'verify_vvpat',
                             'hear_beep', 'exit_booth'],
    },
    4: {
        'type': 'precision',
        'target_finger': 'left_index',
        'target_area': 'nail_cuticle_to_tip',
        'ink_properties': {
            'chemical': 'Silver Nitrate',
            'manufacturer': 'Mysore Paints & Varnish Ltd.',
            'duration': '72+ hours',
            'color': '#4A0080',
        },
        'fingers': ['left_thumb', 'left_index', 'left_middle', 'left_ring', 'left_pinky',
                    'right_thumb', 'right_index', 'right_middle', 'right_ring', 'right_pinky'],
        'correct_finger': 'left_index',
        'correct_position': 'nail',
    },
    5: {
        'type': 'document_review',
        'candidates': [
            {
                'id': 'c1', 'name': 'Dr. Meera Joshi', 'age': 42, 'party': 'blue_lotus',
                'education': 'PhD Political Science', 'criminal_record': False,
                'assets_declared': True, 'age_eligible': True,
                'affidavit_complete': True, 'verdict': 'accept',
                'reason': 'Meets all eligibility criteria under RPA 1951.'
            },
            {
                'id': 'c2', 'name': 'Vikram Singh', 'age': 23, 'party': 'golden_gear',
                'education': 'B.Tech Computer Science', 'criminal_record': False,
                'assets_declared': True, 'age_eligible': False,
                'affidavit_complete': True, 'verdict': 'reject',
                'reason': 'Age 23 — below minimum age of 25 for candidacy.'
            },
            {
                'id': 'c3', 'name': 'Lakshmi Narayan', 'age': 55, 'party': 'rising_sun',
                'education': 'MBA Finance', 'criminal_record': True,
                'criminal_details': 'Convicted under Section 8 of RPA — 3 years sentence',
                'assets_declared': True, 'age_eligible': True,
                'affidavit_complete': True, 'verdict': 'reject',
                'reason': 'Disqualified under Section 8 of RPA 1951.'
            },
            {
                'id': 'c4', 'name': 'Zara Sheikh', 'age': 31, 'party': 'eternal_flame',
                'education': 'LLB Law', 'criminal_record': False,
                'assets_declared': False, 'age_eligible': True,
                'affidavit_complete': False, 'verdict': 'reject',
                'reason': 'Incomplete affidavit — assets not declared.'
            },
        ],
    },
    6: {
        'type': 'placement_puzzle',
        'grid_size': 8,
        'max_booths': 4,
        'radius_km': 2,
        'villages': [
            {'id': 'vil1', 'name': 'Surajpur', 'x': 1, 'y': 1, 'population': 1200},
            {'id': 'vil2', 'name': 'Chandanpur', 'x': 3, 'y': 1, 'population': 800},
            {'id': 'vil3', 'name': 'Govindgarh', 'x': 6, 'y': 2, 'population': 1400},
            {'id': 'vil4', 'name': 'Lakshmipur', 'x': 1, 'y': 5, 'population': 600},
            {'id': 'vil5', 'name': 'Amritsar Tola', 'x': 4, 'y': 4, 'population': 950},
            {'id': 'vil6', 'name': 'Neelgiri', 'x': 7, 'y': 5, 'population': 1100},
            {'id': 'vil7', 'name': 'Rameshwaram', 'x': 2, 'y': 7, 'population': 750},
            {'id': 'vil8', 'name': 'Jyotipur', 'x': 6, 'y': 7, 'population': 500},
        ],
        'solution_positions': [
            {'x': 2, 'y': 1}, {'x': 5, 'y': 3},
            {'x': 1, 'y': 6}, {'x': 7, 'y': 6},
        ],
        'cell_km': 1,
    },
    7: {
        'type': 'checklist_sequence',
        'start_time': '05:30',
        'deadline': '07:00',
        'steps': [
            {'id': 's1', 'action': 'setup_evm', 'label': 'Set up EVM',
             'order': 1, 'time_minutes': 15},
            {'id': 's2', 'action': 'invite_agents', 'label': 'Invite all party agents',
             'order': 2, 'time_minutes': 5},
            {'id': 's3', 'action': 'run_mock_votes', 'label': 'Cast 50 mock votes',
             'order': 3, 'time_minutes': 20},
            {'id': 's4', 'action': 'verify_counts', 'label': 'Verify vote counts match',
             'order': 4, 'time_minutes': 10},
            {'id': 's5', 'action': 'collect_signatures', 'label': 'Collect signatures on Form 16A',
             'order': 5, 'time_minutes': 10},
            {'id': 's6', 'action': 'reset_evm', 'label': 'Reset EVM and seal VVPAT',
             'order': 6, 'time_minutes': 10},
        ],
        'agents': [
            {'name': 'Agent Sharma', 'party': 'blue_lotus'},
            {'name': 'Agent Patel', 'party': 'golden_gear'},
            {'name': 'Agent Devi', 'party': 'rising_sun'},
            {'name': 'Agent Khan', 'party': 'eternal_flame'},
        ],
    },
    8: {
        'type': 'security_sequence',
        'seals': [
            {'id': 'seal1', 'number': 'ECI-2024-A7721', 'position': 'result_section',
             'label': 'Seal the Result Section of Control Unit'},
            {'id': 'seal2', 'number': 'ECI-2024-B3394', 'position': 'ballot_slot',
             'label': 'Seal the Ballot Unit connector slot'},
            {'id': 'seal3', 'number': 'ECI-2024-C5567', 'position': 'vvpat_chamber',
             'label': 'Seal the VVPAT paper drop chamber'},
        ],
        'custody_steps': [
            {'step': 1, 'action': 'apply_seals', 'label': 'Apply all 3 numbered seals'},
            {'step': 2, 'action': 'record_numbers', 'label': 'Record seal numbers in Form 16'},
            {'step': 3, 'action': 'agent_signatures', 'label': 'Get signatures from all agents'},
            {'step': 4, 'action': 'pack_transport', 'label': 'Pack CU in case for transport'},
            {'step': 5, 'action': 'escort_strongroom', 'label': 'Escort to Strong Room'},
        ],
        'correct_seal_order': ['result_section', 'ballot_slot', 'vvpat_chamber'],
    },
}


def get_level_data(level_id: int) -> Optional[Dict[str, Any]]:
    """
    Get interactive data for a level.

    Args:
        level_id: The ID of the level to retrieve.

    Returns:
        The level data dictionary if found, else None.
    """
    return LEVEL_DATA.get(level_id)
