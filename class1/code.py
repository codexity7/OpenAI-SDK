import os 
from dotenv import find_dotenv,load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Agent, Runner


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

agent= Agent(name="Assistant",instructions="You are a Helpful AI Assistant")

result= Runner.run_sync(agent,input="What is the capital of Pakistan?",run_config=run_config)

print(result.final_output)
