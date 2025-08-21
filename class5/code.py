from dataclasses import dataclass
import os
from agents import OpenAIChatCompletionsModel,AsyncOpenAI, RunConfig,Agent, RunContextWrapper, Runner, function_tool, tool
from dotenv import find_dotenv,load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())
gemini_api_key=os.getenv("GEMINI_API_KEY")

external_client=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
run_config=RunConfig(
    model=model,
    tracing_disabled=True
)


# @function_tool(name_override="Fetch_Weather",description_override="fetch weather",strict_mode=True)
# def get_Weather(city:str)->str:
#     """
#     Fetch the weather for the given city

#     Args: city: The city for which the weather is being fetched.

#     """
#     return f"The weather for {city} is sunny."


spanish_agent = Agent(
    name="Spanish agent",
    instructions="You are a Spanish translator. Translate the given text to Spanish and return only the translation.",
    model=model  # Add model to sub-agents
)

french_agent = Agent(
    name="French agent", 
    instructions="You are a French translator. Translate the given text to French and return only the translation.",
    model=model  # Add model to sub-agents
)

# Main orchestrator agent
agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation orchestrator. Use the available tools to translate text. "
        "When a user asks for translation, call the appropriate tool with the text to translate. "
        "If asked for multiple translations, call the relevant tools for each language."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the given text to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french", 
            tool_description="Translate the given text to French",
        ),
    ],
)

result=Runner.run_sync(agent,input="Convert the given text into spanish and french :Hi you are watching codexity",run_config=run_config)

print(result.final_output)

# for tool in agent.tools:
#     print(f"The name of the tool called is {tool.name} and the description of the tool is {tool.description}")
