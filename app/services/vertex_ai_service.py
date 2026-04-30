"""
Vertex AI Service — ECI Constitutional Grounding Agent
Uses Gemini 1.5 Pro to generate explanations grounded in ECI principles.
"""
import logging
import hashlib
import json

logger = logging.getLogger(__name__)

# System prompt that grounds all AI responses in ECI constitutional principles
ECI_SYSTEM_PROMPT = """You are the ECI Constitutional Advisor for LOKTANTRA: The Sovereign Saga, 
an educational election simulator for India.

YOUR MANDATE:
- Ground every explanation in the Election Commission of India's constitutional mandate.
- Reference specific Articles from Part XV of the Indian Constitution (Articles 324-329).
- Explain WHY each democratic process exists, linking it to constitutional principles.
- Use clear, age-appropriate language suitable for both children and adults.
- Be factual, educational, and inspiring about democratic values.
- Keep responses concise (3-5 sentences) but substantive.

KEY CONSTITUTIONAL REFERENCES:
- Article 324: Superintendence, direction, and control of elections vested in ECI
- Article 325: No person excluded from electoral rolls on grounds of religion, race, caste, or sex
- Article 326: Elections on the basis of universal adult suffrage (18+ years)
- Article 327: Power of Parliament to make election laws
- Article 328: Power of State Legislatures regarding elections
- Article 329: Bar to interference by courts in electoral matters

ADDITIONAL PRINCIPLES:
- Model Code of Conduct (MCC): Ensures level playing field during elections
- Representation of the People Act, 1950 & 1951: Qualification/disqualification of candidates
- ECI Guidelines on EVM/VVPAT: Ensuring transparency and verifiability
- 2km polling station rule: Ensuring democratic access for every citizen
- Indelible ink protocol: One-person-one-vote enforcement
- Mock poll protocol: Building multi-party trust through observation
- Chain of custody for Control Units: Integrity of the vote count

FORMAT: Respond with a JSON object containing:
{
  "title": "Brief insight title",
  "explanation": "The constitutional explanation (3-5 sentences)",
  "article_reference": "Primary article or principle referenced",
  "fun_fact": "An interesting related fact"
}"""

# Pre-written fallback explanations when Vertex AI is unavailable
STATIC_EXPLANATIONS = {
    1: {
        "title": "The Guardian of Identity",
        "explanation": "Under Article 325 of the Indian Constitution, no person can be excluded from electoral rolls on grounds of religion, race, caste, or sex. The Electoral Roll is the bedrock of democracy — it ensures every eligible citizen has the right to vote. Verified rolls prevent 'ghost voting' where fictitious names are used to cast fraudulent votes, protecting the sanctity of each genuine voter's choice.",
        "article_reference": "Article 325 — Non-discrimination in Electoral Rolls",
        "fun_fact": "India's electoral roll contains over 950 million voters, making it the largest democratic exercise in human history!"
    },
    2: {
        "title": "The Shield of Silence",
        "explanation": "The 48-hour 'silence period' before polling is mandated by the Model Code of Conduct enforced under Article 324's broad powers. This cooling-off period protects voter autonomy by preventing last-minute propaganda, deepfakes, and emotional manipulation. It gives citizens space to make informed, independent decisions free from campaign pressure.",
        "article_reference": "Article 324 — ECI's Superintendence Powers + Model Code of Conduct",
        "fun_fact": "The silence period also bans opinion polls from being published 48 hours before voting to prevent bandwagon effects!"
    },
    3: {
        "title": "The Digital-Physical Trust Bridge",
        "explanation": "The EVM+VVPAT system exemplifies Article 324's mandate for ECI to ensure free and fair elections through technological innovation. The 3-step process — pressing the ballot button, viewing the VVPAT paper slip for 7 seconds, and hearing the Control Unit's confirmation beep — creates a physical audit trail for every digital vote. This dual verification makes Indian elections both efficient and verifiable.",
        "article_reference": "Article 324 — Superintendence and Control of Elections",
        "fun_fact": "The VVPAT paper slips from 5 randomly selected booths per constituency are physically counted to verify EVM accuracy!"
    },
    4: {
        "title": "The Indelible Promise",
        "explanation": "Indelible ink, applied to the left index finger's nail, is the gold standard for enforcing the one-person-one-vote principle rooted in Article 326's universal adult suffrage. Made with silver nitrate by Mysore Paints & Varnish Ltd., the ink resists washing for 72+ hours, making duplicate voting physically visible. This simple yet brilliant technology has been India's anti-fraud guardian since 1962.",
        "article_reference": "Article 326 — Universal Adult Suffrage",
        "fun_fact": "Mysore Paints & Varnish Ltd. is the sole authorized manufacturer and has supplied indelible ink to over 25 countries!"
    },
    5: {
        "title": "The Transparency Lens",
        "explanation": "Candidate scrutiny is powered by the Representation of the People Act (1951), enacted under Parliament's authority from Article 327. Candidates must be 25+ years old for Lok Sabha/State Assemblies, must disclose criminal records, and file detailed affidavits about assets and education. This transparency ensures voters can make informed choices about their representatives' fitness for office.",
        "article_reference": "Article 327 — Parliament's Power to Make Election Laws",
        "fun_fact": "Since 2003, all candidates must file affidavits disclosing criminal cases, assets, and educational qualifications!"
    },
    6: {
        "title": "Democracy at Your Doorstep",
        "explanation": "The ECI's 2km rule — ensuring no voter travels more than 2 kilometers to reach a polling booth — embodies Article 324's spirit that democracy must come to the citizen, not the other way around. In remote Himalayan villages, dense forests, and island territories, ECI sets up polling stations even for a single voter. This commitment makes Indian elections the most logistically ambitious democratic exercise on Earth.",
        "article_reference": "Article 324 — Ensuring Universal Access to Voting",
        "fun_fact": "In 2019, a polling booth was set up in the Gir Forest for a single voter — a temple priest living in the wilderness!"
    },
    7: {
        "title": "The Dawn of Trust",
        "explanation": "The mock poll protocol, conducted at 5:30 AM before actual voting begins, is a trust-building ritual mandated by ECI under Article 324. Representatives from all contesting parties witness 50 test votes being cast on the EVM, verify the counts match, and sign off before the machines are reset to zero. This multi-party observation converts potential skepticism into documented, witnessed confidence in the system.",
        "article_reference": "Article 324 — Building Multi-party Trust in Electoral Process",
        "fun_fact": "The mock poll results are recorded in Form 16A, signed by all present agents, creating an unbreakable chain of witness!"
    },
    8: {
        "title": "The Unbreakable Chain",
        "explanation": "After voting ends, the Control Unit is sealed with specially numbered tags in the presence of polling agents — a chain-of-custody protocol under ECI's Article 324 authority. Each seal number is recorded, the strong room is double-locked with keys held by different officials, and 24/7 CCTV surveillance begins. This rigorous custody chain ensures that from the last vote cast to the final count, no tampering is physically possible.",
        "article_reference": "Article 324 — Integrity of Electoral Process",
        "fun_fact": "Strong rooms are guarded by Central Armed Police Forces, and candidates can appoint their own agents to watch the sealed rooms!"
    }
}


class VertexAIService:
    """Manages Vertex AI Gemini integration with ECI grounding."""

    def __init__(self, app=None):
        self.model = None
        self.enabled = False
        self._cache = {}

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Vertex AI client if enabled."""
        self.model_name = app.config.get('VERTEX_AI_MODEL', 'gemini-1.5-pro')

        if app.config.get('ENABLE_VERTEX_AI'):
            try:
                import vertexai
                from vertexai.generative_models import GenerativeModel

                project_id = app.config.get('GCP_PROJECT_ID')
                location = app.config.get('VERTEX_AI_LOCATION', 'us-central1')

                vertexai.init(project=project_id, location=location)
                self.model = GenerativeModel(
                    self.model_name,
                    system_instruction=ECI_SYSTEM_PROMPT
                )
                self.enabled = True
                logger.info("Vertex AI initialized: %s @ %s/%s",
                            self.model_name, project_id, location)
            except Exception as e:
                logger.warning("Vertex AI unavailable, using static fallbacks: %s", e)
                self.enabled = False
        else:
            logger.info("Vertex AI disabled, using static explanations")

    def explain_why(self, level_id, context=None):
        """
        Generate a grounded 'Why' explanation for a level.

        Args:
            level_id: The level number (1-8)
            context: Optional additional context about the player's actions

        Returns:
            dict with title, explanation, article_reference, fun_fact
        """
        # Check cache first
        cache_key = self._make_cache_key(level_id, context)
        if cache_key in self._cache:
            logger.info("Cache hit for explanation: level %d", level_id)
            return self._cache[cache_key]

        if self.enabled and self.model:
            try:
                prompt = self._build_prompt(level_id, context)
                response = self.model.generate_content(prompt)

                # Parse JSON response
                text = response.text.strip()
                # Handle markdown code blocks in response
                if text.startswith('```'):
                    text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()

                result = json.loads(text)
                self._cache[cache_key] = result
                logger.info("Vertex AI explanation generated for level %d", level_id)
                return result

            except Exception as e:
                logger.error("Vertex AI explain_why failed for level %d: %s", level_id, e)

        # Fallback to static explanations
        return self._get_static_explanation(level_id)

    def _build_prompt(self, level_id, context=None):
        """Build a level-specific prompt for the AI."""
        level_prompts = {
            1: "Explain WHY verified electoral rolls prevent 'Ghost Voting' and protect voter identity.",
            2: "Explain WHY the 48-hour silence period before elections protects voter autonomy from deepfakes and propaganda.",
            3: "Explain WHY the 3-step EVM + VVPAT system creates a trustworthy physical audit trail for digital votes.",
            4: "Explain WHY indelible ink on the voter's finger is the gold standard for enforcing one-person-one-vote.",
            5: "Explain WHY candidate scrutiny (age 25+, criminal record disclosure, affidavits) ensures transparency in leadership.",
            6: "Explain WHY the 2km polling booth rule ensures democracy must come to every citizen, even in remote areas.",
            7: "Explain WHY the mock poll protocol at 6 AM with party agents builds multi-party trust and observation.",
            8: "Explain WHY the seal-and-custody chain for Control Units ensures the integrity of votes from booth to counting hall.",
        }

        prompt = level_prompts.get(level_id, f"Explain the democratic principle behind Level {level_id}.")

        if context:
            prompt += f"\n\nPlayer context: {context}"

        return prompt

    def _get_static_explanation(self, level_id):
        """Return a pre-written explanation for the given level."""
        return STATIC_EXPLANATIONS.get(level_id, {
            "title": "Democratic Principle",
            "explanation": "Every aspect of India's electoral process is designed to uphold the constitutional mandate of free, fair, and accessible elections for all citizens.",
            "article_reference": "Part XV — Articles 324-329",
            "fun_fact": "India conducts the largest democratic election in the world!"
        })

    def _make_cache_key(self, level_id, context):
        """Generate a cache key for an explanation request."""
        raw = f"{level_id}:{context or ''}"
        return hashlib.md5(raw.encode()).hexdigest()
