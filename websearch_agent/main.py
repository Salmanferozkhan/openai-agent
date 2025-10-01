import os
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled,function_tool
from dotenv import load_dotenv,find_dotenv
from tavily import TavilyClient


load_dotenv(find_dotenv())
set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client)

@function_tool
def websearch(query:str):
 """
 Search the web for the query
 """
 print(f"TOOL CALLING - Searching the web for {query}")
 response = tavily_client.search(f"{query}")
 print(response)
 return response

agent:Agent = Agent(name="WebSearch", model=llm_model, tools=[websearch])

result = Runner.run_sync(agent,"Flight Karachi to Jeddah lowest price in PKR")

print(result.final_output)