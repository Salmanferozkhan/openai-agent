import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled

load_dotenv(find_dotenv())
set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
llm_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

agent = Agent(name="Assistant", model=llm_model)

result = Runner.run_sync(agent, "Hello")

print(result.final_output)