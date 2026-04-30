"""
Level Definitions — Metadata and configuration for all 8 levels.
"""

PARTIES = {
    'blue_lotus': {
        'name': 'The Blue Lotus Party',
        'symbol': 'blue-lotus',
        'icon': '\u2727',
        'color': '#3B82F6',
        'slogan': 'Wisdom Through Unity',
        'manifesto': 'Committed to social harmony and traditional wisdom. We believe in building a future where unity is our greatest strength.',
    },
    'golden_gear': {
        'name': 'The Golden Gear Party',
        'symbol': 'golden-gear',
        'icon': '\u2699',
        'color': '#F59E0B',
        'slogan': 'Progress Through Industry',
        'manifesto': 'Driving economic growth through technological innovation and industrial excellence. Efficiency is our core ideology.',
    },
    'rising_sun': {
        'name': 'The Rising Sun Party',
        'symbol': 'rising-sun',
        'icon': '\u2600',
        'color': '#EF4444',
        'slogan': 'A New Dawn for All',
        'manifesto': 'Empowering the common citizen through radical transparency and social welfare. A new dawn of equality for every person.',
    },
    'eternal_flame': {
        'name': 'The Eternal Flame Party',
        'symbol': 'eternal-flame',
        'icon': '\u2B50',
        'color': '#8B5CF6',
        'slogan': 'Light That Never Fades',
        'manifesto': 'Protecting the sovereignty and environmental heritage of the nation. A flame that guards our future generations.',
    },
}

LEVELS = {
    1: {
        'id': 1,
        'title': 'The Electoral Maze',
        'subtitle': 'Identity',
        'saga': 'voter',
        'saga_label': 'The Voter Saga',
        'description': 'Navigate the Electoral Maze to find and verify voter identities. Match voters to their correct entries and expose ghost voters hiding in the rolls.',
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
        'description': 'The 48-hour silence period has begun. Identify deepfake news from real news before voters are misled. Swipe right for REAL, left for FAKE.',
        'objective': 'Correctly classify 8 news items as Real or Deepfake within the silence window.',
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
        'description': 'Step into the voting booth and cast your vote using the EVM + VVPAT system. Follow the 3-step process exactly as real voters do.',
        'objective': 'Complete the 3-step voting process: Press BU button, verify VVPAT slip, confirm CU beep.',
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
        'description': 'Apply the indelible ink to mark the voter. The ink must go on the correct finger, in the correct position, to prevent duplicate voting.',
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
        'description': 'You are the Returning Officer. Examine candidate affidavits for eligibility — check age, criminal records, and mandatory declarations.',
        'objective': 'Review 4 candidate affidavits and correctly accept or reject each based on legal criteria.',
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
        'description': 'Place polling booths across the district map so every village is within 2km of a booth. Democracy must reach every doorstep.',
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
        'description': 'It is 5:30 AM on election day. Coordinate the mock poll: set up the EVM, run test votes, verify counts, and get all party agents to sign off.',
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
        'description': 'Voting has ended. Secure the Control Unit with numbered seals, log seal numbers, and prepare for transport to the strong room.',
        'objective': 'Apply 3 seals in the correct positions, record all numbers, and complete the chain-of-custody form.',
        'insight_title': 'The Chain of Custody',
        'eci_article': 'Article 324',
        'max_time': 90,
        'difficulty': 'Hard',
        'color': '#DC2626',
        'icon': '\U0001F512',
    },
}


def get_level(level_id):
    """Get level metadata by ID."""
    return LEVELS.get(level_id)


def get_all_levels():
    """Get all level metadata."""
    return LEVELS


def get_saga_levels(saga):
    """Get levels filtered by saga type ('voter' or 'officer')."""
    return {k: v for k, v in LEVELS.items() if v['saga'] == saga}
