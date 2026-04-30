"""
Vertex AI Service — ECI Constitutional Grounding Agent
Uses Gemini 1.5 Pro to generate explanations grounded in ECI principles.
"""
import logging
import hashlib
import json
from typing import Dict, Any, Optional
from flask import Flask

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
STATIC_EXPLANATIONS: Dict[int, Dict[str, str]] = {
    1: {
        "title": "The Guardian of Identity",
        "explanation": ("Under Article 325, no person can be excluded from electoral rolls on "
                        "grounds of religion, race, caste, or sex. The Electoral Roll ensures "
                        "every eligible citizen has the right to vote. Verified rolls prevent "
                        "'ghost voting', protecting the sanctity of each voter's choice."),
        "article_reference": "Article 325 — Non-discrimination in Electoral Rolls",
        "fun_fact": "India's electoral roll contains over 950 million voters!"
    },
    2: {
        "title": "The Shield of Silence",
        "explanation": ("The 48-hour 'silence period' is mandated by the MCC enforced under "
                        "Article 324. This cooling-off period protects voter autonomy by "
                        "preventing propaganda and deepfakes, giving citizens space to make "
                        "informed decisions free from campaign pressure."),
        "article_reference": "Article 324 — ECI's Superintendence Powers + MCC",
        "fun_fact": "The silence period also bans opinion polls from being published!"
    },
    3: {
        "title": "The Digital-Physical Trust Bridge",
        "explanation": ("The EVM+VVPAT system ensures free and fair elections through innovation. "
                        "The 3-step process — pressing the button, viewing the paper slip, and "
                        "hearing the beep — creates a physical audit trail. This dual "
                        "verification makes Indian elections efficient and verifiable."),
        "article_reference": "Article 324 — Superintendence and Control of Elections",
        "fun_fact": "VVPAT slips from 5 randomly selected booths are physically counted!"
    },
    4: {
        "title": "The Indelible Promise",
        "explanation": ("Indelible ink is the gold standard for enforcing one-person-one-vote "
                        "rooted in Article 326. Made with silver nitrate, it resists washing "
                        "for 72+ hours, making duplicate voting physically visible. This "
                        "technology has been India's anti-fraud guardian since 1962."),
        "article_reference": "Article 326 — Universal Adult Suffrage",
        "fun_fact": "The ink is manufactured by Mysore Paints & Varnish Ltd.!"
    },
    5: {
        "title": "The Transparency Lens",
        "explanation": ("Scrutiny is powered by the RPA (1951), enacted under Article 327. "
                        "Candidates must be 25+, disclose criminal records, and file "
                        "detailed affidavits. This transparency ensures voters can make "
                        "informed choices about their representatives."),
        "article_reference": "Article 327 — Parliament's Power to Make Election Laws",
        "fun_fact": "Since 2003, candidates must disclose assets and education!"
    },
    6: {
        "title": "Democracy at Your Doorstep",
        "explanation": ("The 2km rule embodies Article 324's spirit that democracy must come "
                        "to the citizen. In remote villages and forests, ECI sets up booths "
                        "even for a single voter. This commitment makes Indian elections "
                        "the most logistically ambitious exercise on Earth."),
        "article_reference": "Article 324 — Ensuring Universal Access to Voting",
        "fun_fact": "In 2019, a booth was set up in the Gir Forest for a single voter!"
    },
    7: {
        "title": "The Dawn of Trust",
        "explanation": ("The mock poll protocol at 5:30 AM is a trust-building ritual mandated "
                        "by ECI. Party agents witness 50 test votes, verify counts, and "
                        "sign off before machines are reset. This observation converts "
                        "potential skepticism into documented, witnessed confidence."),
        "article_reference": "Article 324 — Building Multi-party Trust",
        "fun_fact": "Mock poll results are recorded in Form 16A, signed by all agents!"
    },
    8: {
        "title": "The Unbreakable Chain",
        "explanation": ("After voting, the Control Unit is sealed with numbered tags in the "
                        "presence of agents. Each seal number is recorded, and the strong "
                        "room is double-locked and guarded 24/7. This custody chain ensures "
                        "no tampering is physically possible."),
        "article_reference": "Article 324 — Integrity of Electoral Process",
        "fun_fact": "Strong rooms are guarded by Central Armed Police Forces!"
    }
}


class VertexAIService:
    """Manages Vertex AI Gemini integration with ECI grounding and local fallbacks."""

    def __init__(self, app: Optional[Flask] = None):
        self.model: Any = None
        self.enabled: bool = False
        self._cache: Dict[str, Dict[str, str]] = {}

        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize Vertex AI client if enabled in configuration.

        Args:
            app: The Flask application instance.
        """
        self.model_name = app.config.get('VERTEX_AI_MODEL', 'gemini-1.5-pro')

        if app.config.get('ENABLE_VERTEX_AI'):
            try:
                import vertexai  # pylint: disable=import-outside-toplevel,import-error
                from vertexai.generative_models import GenerativeModel  # pylint: disable=import-outside-toplevel,import-error

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
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.warning("Vertex AI unavailable, using static fallbacks: %s", e)
                self.enabled = False
        else:
            logger.info("Vertex AI disabled, using static explanations")

    def explain_why(self, level_id: int, context: Optional[str] = None) -> Dict[str, str]:
        """
        Generate a grounded 'Why' explanation for a level using AI or static fallback.

        Args:
            level_id: The level number (1-8).
            context: Optional additional context about the player's actions.

        Returns:
            A dictionary with 'title', 'explanation', 'article_reference', and 'fun_fact'.
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

            except Exception as e: # pylint: disable=broad-exception-caught
                logger.error("Vertex AI explain_why failed for level %d: %s", level_id, e)

        # Fallback to static explanations
        return self._get_static_explanation(level_id)

    def _build_prompt(self, level_id: int, context: Optional[str] = None) -> str:
        """Build a level-specific prompt for the AI."""
        level_prompts = {
            1: "Explain WHY verified electoral rolls prevent 'Ghost Voting'.",
            2: "Explain WHY the 48-hour silence period protects voter autonomy.",
            3: "Explain WHY the 3-step EVM + VVPAT system creates a physical audit trail.",
            4: "Explain WHY indelible ink is the gold standard for one-person-one-vote.",
            5: "Explain WHY candidate scrutiny ensures transparency in leadership.",
            6: "Explain WHY the 2km polling booth rule ensures democracy reaches everyone.",
            7: "Explain WHY the mock poll protocol builds multi-party trust.",
            8: "Explain WHY the seal-and-custody chain ensures the integrity of votes.",
        }

        prompt = level_prompts.get(
            level_id,
            f"Explain the democratic principle behind Level {level_id}."
        )

        if context:
            prompt += f"\n\nPlayer context: {context}"

        return prompt

    def _get_static_explanation(self, level_id: int) -> Dict[str, str]:
        """Return a pre-written explanation for the given level."""
        return STATIC_EXPLANATIONS.get(level_id, {
            "title": "Democratic Principle",
            "explanation": (
                "Every aspect of India's electoral process is designed "
                "to uphold the constitutional mandate of free, fair, "
                "and accessible elections for all citizens."
            ),
            "article_reference": "Part XV — Articles 324-329",
            "fun_fact": "India conducts the largest democratic election!"
        })

    def _make_cache_key(self, level_id: int, context: Optional[str]) -> str:
        """Generate a stable cache key for an explanation request."""
        raw = f"{level_id}:{context or ''}"
        return hashlib.md5(raw.encode()).hexdigest()
