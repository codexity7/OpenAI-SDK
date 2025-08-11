import os
from agents import (
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    RunConfig,
    Agent,
    Runner
)
from dotenv import find_dotenv, load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from openai.types.runs import (
    MessageOutputItem,
    ToolCallItem,
    ToolCallOutputItem
)

# Load API key
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# External client for Gemini
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model config
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Run config
run_config = RunConfig(
    model=model,
    tracing_disabled=True
)

# Agent
agent = Agent(name="Assistant", instructions="You are a helpful Assistant.")

# Main streaming function
async def main():
    result = Runner.run_streamed(agent, "Write an essay on AI", run_config=run_config)

    async for event in result.stream_events():
        # --- RAW LLM TOKEN STREAM ---
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

        # --- COMPLETED MESSAGE OUTPUT ---
        elif event.type == "run_item_streamed" and isinstance(event.data, MessageOutputItem):
            print(f"\n[Message Output]: {event.data.content}")

        # --- TOOL CALL DETECTED ---
        elif event.type == "run_item_streamed" and isinstance(event.data, ToolCallItem):
            print(f"\n[Tool Call]: {event.data.name} with arguments {event.data.arguments}")

        # --- TOOL CALL RESULT ---
        elif event.type == "run_item_streamed" and isinstance(event.data, ToolCallOutputItem):
            print(f"\n[Tool Result]: {event.data.output}")

        # --- AGENT HANDOFF ---
        elif event.type == "run_item_streamed":
            print(f"\n[Agent Handoff or Other Run Item]: {event.data}")

# Run the async loop
import asyncio
asyncio.run(main())
