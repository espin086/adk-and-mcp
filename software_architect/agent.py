import asyncio
import os
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent, SequentialAgent
from google.genai import types
from google.adk.runners import InMemoryRunner
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools.tool_context import ToolContext
from typing import AsyncGenerator, Optional
from google.adk.events import Event, EventActions

# --- Constants ---
APP_NAME = "plantuml_architect_v1" # New App Name
USER_ID = "dev_user_01"
SESSION_ID_BASE = "plantuml_loop_session" # New Base Session ID
GEMINI_MODEL = "gemini-2.5-flash"
STATE_INITIAL_TOPIC = "initial_topic"

# --- State Keys ---
STATE_CURRENT_DOC = "current_document"
STATE_CRITICISM = "criticism"
# Define the exact phrase the Critic should use to signal completion
COMPLETION_PHRASE = "No major issues found."

# --- Tool Definition ---
def exit_loop(tool_context: ToolContext):
  """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
  print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
  tool_context.actions.escalate = True
  # Return empty dict as tools should typically return JSON-serializable output
  return {}



# --- PROMPTS ---

# --- PROMPTS ---

PROMPT_INPUT_MAPPING = """
You are a simple passthrough agent. Your only job is to take the user's input and place it into the 'initial_topic' state.

Output the user input exactly as you received it, with no changes or additions.
"""

PROMPT_INITIAL_WRITER = f"""
You are an expert Software Architect. Your task is to create an initial architectural diagram in PlantUML based on the user's request.

**User Request:**
{{{{initial_topic}}}}

**Styling Requirements:**
- The diagram must have a professional, polished appearance.
- You **MUST** create a title for the diagram based on the user's request.
- You **MUST** include the following `skinparam` block at the beginning of your PlantUML code to enforce the style. This style removes borders, sets arrow colors to black, and increases title size.

```plantuml
' Style Settings
title
<size:20>{{{{initial_topic}}}}</size>
end title

skinparam handwritten false
skinparam roundcorner 5
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam defaultFontSize 12
skinparam arrowColor black
skinparam titleFontSize 20

' Color Palette (Borders are same as background to remove outlines)
skinparam rectangle {{
  BackgroundColor lightblue
  BorderColor lightblue
}}
skinparam component {{
  BackgroundColor lightblue
  BorderColor lightblue
}}
skinparam database {{
  BackgroundColor lightgray
  BorderColor lightgray
}}
skinparam actor {{
  BackgroundColor lightgray
  BorderColor lightgray
}}
```

**Instructions:**
- Generate a complete PlantUML diagram that represents the core components and relationships described in the user's request.
- Ensure the diagram starts with `@startuml`, includes the `title` block, and the full `skinparam` styling block provided above.
- The diagram must end with `@enduml`.
- Output *only* the raw PlantUML code. Do not include markdown code fences (like ```plantuml) or any other explanations.
"""

PROMPT_CRITIC = f"""You are an expert Software Architect and PlantUML code reviewer. Your goal is to provide concise, actionable feedback on a PlantUML diagram draft.

    **Initial User Request:**
    ```
    {{{{initial_topic}}}}
    ```

    **PlantUML Diagram to Review:**
    ```plantuml
    {{{{current_document}}}}
    ```

    **Task:**
    Review the PlantUML diagram against the initial user request. Check for:
    1.  **Syntax Correctness:** Is the PlantUML syntax valid?
    2.  **Component Accuracy:** Does the diagram include all the key components mentioned in the request?
    3.  **Relationship Clarity:** Are the relationships and data flows between components logical and clearly represented?
    4.  **Styling Requirements:** Does the diagram have a large title? Does it include a `skinparam` block that removes box outlines (border color same as background) and sets arrow color to black?
    5.  **Completeness:** Is the diagram a reasonable interpretation of the user's request?

    **Response Format:**
    -   IF you find specific, critical issues (e.g., "Missing the database component," "Arrows are red, should be black," "Box outlines are visible"), provide a brief, one or two-line critique.
    -   ELSE IF the diagram is a solid and complete representation of the request with no major errors:
        Respond *exactly* with the phrase "{COMPLETION_PHRASE}" and nothing else.

    Output only the critique OR the exact completion phrase.
"""


PROMPT_REFINER = f"""
You are a Software Architect AI. Your task is to refine a PlantUML diagram based on a critique OR to finalize the process.

    **Current PlantUML Diagram:**
    ```plantuml
    {{{{current_document}}}}
    ```

    **Critique/Suggestions:**
    {{{{criticism}}}}

    **Task:**
    Carefully analyze the 'Critique/Suggestions'.

    -   IF the critique is *exactly* "{COMPLETION_PHRASE}":
        You **MUST** call the 'exit_loop' function immediately. Do not output any text.

    -   ELSE (the critique contains actionable feedback):
        Apply the suggestions to improve the 'Current PlantUML Diagram'.
        **Crucially, you must preserve the polished styling.** This includes the large title and the `skinparam` settings (no outlines, black arrows). If the styling was missing or incorrect, re-insert the correct styling block.
        Output *only* the complete, refined PlantUML code. Ensure it starts with `@startuml` and ends with `@enduml`.

    Do not add explanations. Either output the refined PlantUML code OR call the `exit_loop` function.
"""


# --- Agent Definitions ---

# STEP 1: Input Mapping Agent (Handles initial user query)
input_mapping_agent = LlmAgent(
    name="InputMapper",
    model=GEMINI_MODEL,
    include_contents="default",
    instruction=PROMPT_INPUT_MAPPING,
    description="Maps the initial user query to the 'initial_topic' state variable.",
    output_key=STATE_INITIAL_TOPIC,
)

# STEP 2: Initial Writer Agent (Runs ONCE at the beginning)
initial_writer_agent = LlmAgent(
    name="InitialWriterAgent",
    model=GEMINI_MODEL,
    include_contents='none',
    instruction=PROMPT_INITIAL_WRITER,
    description="Writes the initial PlantUML diagram based on the user's request.",
    output_key=STATE_CURRENT_DOC
)

# STEP 2a: Critic Agent (Inside the Refinement Loop)
critic_agent_in_loop = LlmAgent(
    name="CriticAgent",
    model=GEMINI_MODEL,
    include_contents='none',
    instruction=PROMPT_CRITIC,
    description="Reviews the current PlantUML diagram, providing critique if improvements are needed, otherwise signals completion.",
    output_key=STATE_CRITICISM
)


# STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
refiner_agent_in_loop = LlmAgent(
    name="RefinerAgent",
    model=GEMINI_MODEL,
    # Relies solely on state via placeholders
    include_contents='none',
    instruction=PROMPT_REFINER,
    description="Refines the PlantUML diagram based on critique, or calls exit_loop if critique indicates completion.",
    tools=[exit_loop], # Provide the exit_loop tool
    output_key=STATE_CURRENT_DOC # Overwrites state['current_document'] with the refined version
)


# STEP 2: Refinement Loop Agent
refinement_loop = LoopAgent(
    name="RefinementLoop",
    # Agent order is crucial: Critique first, then Refine/Exit
    sub_agents=[
        critic_agent_in_loop,
        refiner_agent_in_loop,
    ],
    max_iterations=5 # Limit loops
)

# STEP 3: Overall Sequential Pipeline
# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = SequentialAgent(
    name="IterativePlantumlPipeline",
    sub_agents=[
        input_mapping_agent,  # NEW: First, map the user input to state
        initial_writer_agent, # Then, run the writer
        refinement_loop       # Finally, run the critique/refine loop
    ],
    description="Generates an initial PlantUML diagram and then iteratively refines it with critique using an exit tool."
)


