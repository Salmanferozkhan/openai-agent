import os
from dotenv import load_dotenv,find_dotenv
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,RunConfig

load_dotenv(find_dotenv())
#set_tracing_disabled(True)

# 1. External Client Which Provider
external_client :AsyncOpenAI = AsyncOpenAI(
    api_key = os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 2. Which LLM Model Using?

llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client = external_client
)

#3. Run Config
config :RunConfig = RunConfig(
    model = llm,
    model_provider= external_client,
    tracing_disabled= True
)

# 3. Agent

agent :Agent= Agent(
    name="Assistant"
)

# 4. Run

result = Runner.run_sync(
    agent,"Hello",run_config = config
)
print(result.final_output)