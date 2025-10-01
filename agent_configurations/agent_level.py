import os
from dotenv import load_dotenv,find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled

load_dotenv(find_dotenv())
set_tracing_disabled(True)


# 1. Which LLM Service/Provider ?
external_client : AsyncOpenAI = AsyncOpenAI(
    api_key = os.getenv("GEMINI_API_KEY"),
   base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# 3. Agent 
agent : Agent = Agent(
        name="Assistant",
        #instructions="You only respond in haikus.",
        model=llm_model,
    )

# 4. To Run Agent Use Runner.run_sync

result = Runner.run_sync(
    agent,"Hello"
) 

print(result.final_output)
