import logging
from google.adk.agents import LlmAgent


# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GEMINI_2_FLASH = "gemini-2.0-flash"

PROMPT = """
You are a story reviser. Revise the story provided in
session state with key 'current_story', based on the criticism in
session state with key 'criticism'. Output only the revised story.
"""


reviser = LlmAgent(
    name="Reviser",
    model=GEMINI_2_FLASH,
    instruction=PROMPT,
    input_schema=None,
    output_key="current_story",  # Overwrites the original story
)