import logging
from google.adk.agents import LlmAgent


# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GEMINI_2_FLASH = "gemini-2.0-flash"

PROMPT = """
You are a story critic. Review the story provided in
session state with key 'current_story'. Provide 1-2 sentences of constructive criticism
on how to improve it. Focus on plot or character.
"""


critic = LlmAgent(
    name="Critic",
    model=GEMINI_2_FLASH,
    instruction=PROMPT,
    input_schema=None,
    output_key="criticism",  # Key for storing criticism in session state
)