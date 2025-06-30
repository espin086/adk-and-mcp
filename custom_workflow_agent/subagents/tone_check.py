import logging
from google.adk.agents import LlmAgent


# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GEMINI_2_FLASH = "gemini-2.0-flash"

PROMPT = """You are a tone analyzer. Analyze the tone of the story
provided in session state with key 'current_story'. Output only one word: 'positive' if
the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
otherwise."""

tone_check = LlmAgent(
    name="ToneCheck",
    model=GEMINI_2_FLASH,
    instruction=PROMPT,
    input_schema=None,
    output_key="tone_check_result", # This agent's output determines the conditional flow
)