import logging
from google.adk.agents import LlmAgent


# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GEMINI_2_FLASH = "gemini-2.0-flash"

PROMPT = """
You are a grammar checker. Check the grammar of the story
provided in session state with key 'current_story'. Output only the suggested
corrections as a list, or output 'Grammar is good!' if there are no errors.
"""

grammar_check = LlmAgent(
    name="GrammarCheck",
    model=GEMINI_2_FLASH,
    instruction=PROMPT,
    input_schema=None,
    output_key="grammar_suggestions",
)