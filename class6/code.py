import os
from dotenv import find_dotenv,load_dotenv
from agents import OpenAIChatCompletionsModel,AsyncOpenAI, RunConfig,Agent, Runner, function_tool,handoff

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
def get_order_status(order_id: str)-> str:
    return f"The status of the order {order_id} is pending"

@function_tool
def refund_order(order_id: str)-> str:
    return f"The order {order_id} has been refunded"

Order_agent=Agent(name="Codexity",instructions="You are an order agent that can help with orders",tools=[get_order_status])
Refund_agent=Agent(name="Refund Agent",instructions="You are a refund agent that can help with refunds",tools=[refund_order])

agent1=handoff(agent=Order_agent,
tool_name_override="getOrderStatus",tool_description_override="You are an order agent that help with orders")

Triage_Agent=Agent(name="Triage Agent",instructions="You are a triage agent that can help with orders and refunds",
handoffs=[agent1,Refund_agent]
)

result=Runner.run_sync(Triage_Agent,input="What is the status of the order id 124567890",run_config=run_config)
print(result.last_agent.name)
