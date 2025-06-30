import logging
from google.adk.agents import LlmAgent


# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GEMINI_2_FLASH = "gemini-2.0-flash"

story_generator = LlmAgent(
    name="StoryGenerator",
    model=GEMINI_2_FLASH,
    instruction="""You are a story writer. Write a short story (around 100 words) about a cat,
based on the topic provided in session state with key 'topic'""",
    input_schema=None,
    output_key="current_story",  # Key for storing output in session state
)