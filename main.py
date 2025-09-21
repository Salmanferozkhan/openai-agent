from os import name
from agents import Agent,Runner,OpenAIChatCompletionsModel, AsyncOpenAI
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv());



# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

agent:Agent = Agent(
    name = "Assistant",
    #instructions = "You are a assistant agent",
    model=llm_model
)

result = Runner.run_sync(agent,"Hello")
print(result.final_output)