from os import name
from agents import Agent,Runner,OpenAIChatCompletionsModel, AsyncOpenAI
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

# Check if API key is set
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: GEMINI_API_KEY environment variable is not set!")
    print("Please set your Gemini API key:")
    print("1. Create a .env file in this directory")
    print("2. Add: GEMINI_API_KEY=your_api_key_here")
    print("3. Or set it as an environment variable")
    exit(1)

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

agent:Agent = Agent(
    name = "Assistant",
    instructions = "Top 3 AI agents framework 2025 which has less abstraction",
    model=llm_model
)

print("🤖 Running agent...")
result = Runner.run_sync(agent,"Hello")
print("✅ Agent response:")
print(result.final_output)