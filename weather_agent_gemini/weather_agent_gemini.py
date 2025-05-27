from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    assert isinstance(city, str), "City must be a string"
    logger.info("--- Tool Call: Getting weather for %s ---", city)
    city_normalized = city.lower().replace(" ", "")


    # Mock the weather data for newyork, london, tokyo as a dictionary
    weather_data = {
        "newyork": {
            "status": "success",
            "report": "The weather in New York is sunny with a temperature of 25°C."
        },
        "london": {
            "status": "success",
            "report": "It's cloudy in London with a temperature of 15°C."
        },
        "tokyo": {
            "status": "success",
            "report": "Tokyo is experiencing light rain and a temperature of 18°C."
        }
    } 

    if city_normalized in weather_data:
        return weather_data[city_normalized]
    else:
        return {
            "status": "error",
            "error_message": f"The weather for {city} not available."
        }

# # Example tool usage (optional tests)
# print(get_weather("New York"))
# print(get_weather("London"))
# print(get_weather("Tokyo"))
# print(get_weather("Paris")) # this should return an error

AGENT_MODEL = MODEL_GEMINI_2_0_FLASH


DESCRIPTION = """
You are a helpful weather assistant.
"""


INSTRUCTIONS = """
You are a helpful weather assistant. When the user asks for the weather in a specific city, 
use the 'get_weather' tool to find the information. 
If the tool returns an error, inform the user politely. 
If the tool is successful, present the weather report clearly.
You can use the 'get_weather' tool to get the weather information for a specific city.


"""

root_agent = Agent(
    name="weather_agent_v1_gemini",
    model=AGENT_MODEL,
    description=DESCRIPTION,
    instruction=INSTRUCTIONS,
    tools=[get_weather],
    
    )