import os

from dotenv import find_dotenv,load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner, function_tool


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

@function_tool
def getWeather(city:str)->str:
    return f"The weather for {city} is sunny"

agent=Agent(name="Assitant",instructions="You are a helpful Assitant",tools=[getWeather],max_turns=2)


#Running Synchronously
result= Runner.run_sync(agent,"What is the weather of Karachi",run_config=run_config,
)
print(result.last_agent.name)

#Running Asynchronous

import asyncio

async def main():
    result = await Runner.run(agent, "What is the weather of Lahore", run_config=run_config)
    print(result.last_agent.name)

asyncio.run(main())
    

