import os 
from dotenv import find_dotenv,load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Agent, Runner, function_tool, handoff
from pydantic import BaseModel


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
    tracing_disabled=False
)

@function_tool
def getWeather(city:str)->str:
    return f"The weather for {city} is sunny"

@function_tool
def sum(a:int,b:int)->str:
    return f" The sum of {a} and {b} is {a+b}!!!!"



coding_agent= Agent(name="Coding Agent",
instructions="You are a coding expert. Explain everything with code.",
handoff_description="You respond whenever there is a coding question.")


#coding=coding_agent.as_tool(tool_name="Coding_tool",
#tool_description="This will be invoked whenever theres a query related to coding")


agent= Agent(name="Assistant",
instructions="You are a helpful Assistant that can delegate to other agents according to their expertise",
handoff=[coding_agent],
tools=[getWeather,sum,],
tool_use_behavior="stop_on_first_tool")

result = Runner.run_sync(agent,"explain for loop in python",run_config=run_config)

print(f"{result.final_output}")


