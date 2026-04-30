"""
Level Definitions — Metadata and configuration for all 8 levels.
"""
from typing import Dict, Any, Optional

PARTIES: Dict[str, Dict[str, str]] = {
    'blue_lotus': {
        'name': 'The Blue Lotus Party',
        'symbol': 'blue-lotus',
        'icon': '\u2727',
        'color': '#3B82F6',
        'slogan': 'Wisdom Through Unity',
        'manifesto': ('Committed to social harmony and traditional wisdom. '
                      'We believe in building a future where unity is our greatest strength.'),
    },
    'golden_gear': {
        'name': 'The Golden Gear Party',
        'symbol': 'golden-gear',
        'icon': '\u2699',
        'color': '#F59E0B',
        'slogan': 'Progress Through Industry',
        'manifesto': ('Driving economic growth through technological innovation and industrial '
                      'excellence. Efficiency is our core ideology.'),
    },
    'rising_sun': {
        'name': 'The Rising Sun Party',
        'symbol': 'rising-sun',
        'icon': '\u2600',
        'color': '#EF4444',
        'slogan': 'A New Dawn for All',
        'manifesto': ('Empowering the common citizen through radical transparency and social welfare. '
                      'A new dawn of equality for every person.'),
    },
    'eternal_flame': {
        'name': 'The Eternal Flame Party',
        'symbol': 'eternal-flame',
        'icon': '\u2B50',
        'color': '#8B5CF6',
        'slogan': 'Light That Never Fades',
        'manifesto': ('Protecting the sovereignty and environmental heritage of the nation. '
                      'A flame that guards our future generations.'),
    },
}

LEVELS: Dict[int, Dict[str, Any]] = {
    1: {
        'id': 1,
        'title': 'The Electoral Maze',
        'subtitle': 'Identity',
        'saga': 'voter',
        'saga_label': 'The Voter Saga',
        'description': ('Navigate the Electoral Maze to find and verify voter identities. '
                        'Match voters to their correct entries and expose ghost voters.'),
        'objective': 'Find all 5 legitimate voters in the maze and identify the 2 ghost entries.',
        'insight_title': 'Why Verified Rolls Prevent Ghost Voting',
        'eci_article': 'Article 325',
        'max_time': 120,
        'difficulty': 'Easy',
        'color': '#06B6D4',
        'icon': '\U0001F50D',
    },
    2: {
        'id': 2,
        'title': 'The Great Silence',
        'subtitle': 'The Silence',
        'saga': 'voter',
        'saga_label': 'The Voter Saga',
        'description': ('The 48-hour silence period has begun. Identify deepfake news from real '
                        'news before voters are misled.'),
        'objective': 'Correctly classify 8 news items as Real or Deepfake within the window.',
        'insight_title': 'Protecting Voter Autonomy',
        'eci_article': 'Model Code of Conduct',
        'max_time': 90,
        'difficulty': 'Medium',
        'color': '#8B5CF6',
        'icon': '\U0001F910',
    },
    3: {
        'id': 3,
        'title': 'The Sacred Booth',
        'subtitle': 'The Booth',
        'saga': 'voter',
        'saga_label': 'The Voter Saga',
        'description': ('Step into the voting booth and cast your vote using the EVM + VVPAT system. '
                        'Follow the 3-step process exactly.'),
        'objective': 'Complete the 3-step process: Press button, verify slip, confirm beep.',
        'insight_title': 'The Physical Audit Trail of Digital Votes',
        'eci_article': 'Article 324',
        'max_time': 60,
        'difficulty': 'Easy',
        'color': '#10B981',
        'icon': '\U0001F5F3',
    },
    4: {
        'id': 4,
        'title': 'The Indelible Mark',
        'subtitle': 'The Mark',
        'saga': 'voter',
        'saga_label': 'The Voter Saga',
        'description': ('Apply the indelible ink to mark the voter. Correct finger and position '
                        'prevent duplicate voting.'),
        'objective': 'Apply ink correctly to the left index finger nail from cuticle to tip.',
        'insight_title': 'One Person, One Vote',
        'eci_article': 'Article 326',
        'max_time': 45,
        'difficulty': 'Easy',
        'color': '#6366F1',
        'icon': '\u270B',
    },
    5: {
        'id': 5,
        'title': 'The Scrutiny Chamber',
        'subtitle': 'Scrutiny',
        'saga': 'officer',
        'saga_label': 'The Officer Saga',
        'description': ('You are the Returning Officer. Examine candidate affidavits for '
                        'eligibility — check age, criminal records, and declarations.'),
        'objective': 'Review 4 affidavits and correctly accept or reject each.',
        'insight_title': 'Transparency in Leadership',
        'eci_article': 'Article 327 / RPA 1951',
        'max_time': 150,
        'difficulty': 'Medium',
        'color': '#F59E0B',
        'icon': '\U0001F4CB',
    },
    6: {
        'id': 6,
        'title': 'The 2km Mandate',
        'subtitle': 'The 2km Rule',
        'saga': 'officer',
        'saga_label': 'The Officer Saga',
        'description': ('Place polling booths so every village is within 2km of a booth. '
                        'Democracy must reach every doorstep.'),
        'objective': 'Place 4 booths to cover all 8 villages within the 2km radius constraint.',
        'insight_title': 'Democracy at Every Doorstep',
        'eci_article': 'Article 324',
        'max_time': 180,
        'difficulty': 'Hard',
        'color': '#EF4444',
        'icon': '\U0001F4CD',
    },
    7: {
        'id': 7,
        'title': 'The Dawn Protocol',
        'subtitle': 'Mock Poll',
        'saga': 'officer',
        'saga_label': 'The Officer Saga',
        'description': ('It is 5:30 AM. Coordinate the mock poll: set up EVM, run test votes, '
                        'verify counts, and get agent signatures.'),
        'objective': 'Complete the 6-step mock poll checklist in the correct order before 7 AM.',
        'insight_title': 'Building Trust Through Observation',
        'eci_article': 'Article 324',
        'max_time': 120,
        'difficulty': 'Medium',
        'color': '#F97316',
        'icon': '\U0001F305',
    },
    8: {
        'id': 8,
        'title': 'The Seal of Integrity',
        'subtitle': 'Seal of Integrity',
        'saga': 'officer',
        'saga_label': 'The Officer Saga',
        'description': ('Voting has ended. Secure the Control Unit with numbered seals and '
                        'prepare for transport to the strong room.'),
        'objective': 'Apply 3 seals correctly, record numbers, and complete the custody form.',
        'insight_title': 'The Chain of Custody',
        'eci_article': 'Article 324',
        'max_time': 90,
        'difficulty': 'Hard',
        'color': '#DC2626',
        'icon': '\U0001F512',
    },
}


def get_level(level_id: int) -> Optional[Dict[str, Any]]:
    """
    Get level metadata by ID.

    Args:
        level_id: The ID of the level to retrieve.

    Returns:
        The level metadata dictionary if found, else None.
    """
    return LEVELS.get(level_id)


def get_all_levels() -> Dict[int, Dict[str, Any]]:
    """
    Get all level metadata.

    Returns:
        A dictionary containing all levels.
    """
    return LEVELS


def get_saga_levels(saga: str) -> Dict[int, Dict[str, Any]]:
    """
    Get levels filtered by saga type ('voter' or 'officer').

    Args:
        saga: The saga type to filter by.

    Returns:
        A dictionary of levels matching the saga type.
    """
    return {k: v for k, v in LEVELS.items() if v['saga'] == saga}
