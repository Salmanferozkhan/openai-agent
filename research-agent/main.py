import os
import asyncio
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled,function_tool
from dotenv import load_dotenv,find_dotenv
from tavily import TavilyClient
from openai.types.responses import ResponseTextDeltaEvent
from rich import print


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

instructions="""
You are an AI research assistant tasked with finding and explaining a real-world use case where an agentic AI is being used right now.

1. **Research a real-world use case**: Look for a company or workflow where agentic AI is currently being used. This can be in fields like warehouse robots, customer service automation, fraud detection, etc.

2. **Provide a summary with the following details**:
    - **Company name**: (The name of the company using AI agents)
    - **What problem they had**: (Explain the task that was taking a lot of time or money before the AI agent was introduced)
    - **What the agent does**: (What does the AI agent do, what inputs does it receive, and what outputs does it create?)
    - **Where you found this information**: (Provide a link or source, e.g., a news article, company blog, YouTube video, etc.)

3. **Answer the following 5 questions in detail**:

    **Question 1: What Was the Problem?**
    - What task was taking lots of time/money before the agent was used?
    - How many people were doing this task manually?
    - What was costing the company (e.g., labor costs, time delays, etc.)?

    **Question 2: What Agent Did They Build?**
    - What does the agent do (be specific about its task)?
    - What inputs does the agent receive (e.g., instructions, data, etc.)?
    - What outputs does the agent create (e.g., actions taken, results produced)?

    **Question 3: How Do Humans Stay in Control?**
    - Do humans still make decisions? If so, in what capacity?
    - What do humans check or approve during the process?
    - What happens if something goes wrong (e.g., robot failure, system malfunction)?

    **Question 4: What Results Did They Get?**
    - What improved after the agent was implemented (speed, cost, quality)?
    - By how much did it improve? Provide specific numbers or percentages if available.
    - How did this help the business overall (e.g., increased revenue, reduced costs)?

    **Question 5: Why Did This Work?**
    - Why was this job particularly suited for an AI agent (e.g., repetitive tasks, structured data)?
    - What made it easier or harder than other tasks for the AI to handle?
    - Would this solution work for other companies or industries? Explain why or why not.

4. **Output format**:
   Write your findings in a simple, understandable format that a grade 10 student could easily grasp. Use bullet points for clarity where necessary.
   - Heading 1: Company name and the problem faced
   - Heading 2: What the agent does and how humans stay in control?
   - Heading 3: What measurable results they got
   - Heading 4: Why this matters
   - Heading 5: Include at least ONE source or link to the information used (news article, YouTube video, company report, etc.)

Please provide detailed, but simple explanations. Use clear and concise language. If possible, include any numbers or measurable impacts that show how the agent has made a difference.
"""
agent:Agent = Agent(name="Research", instructions=instructions, model=llm_model, tools=[websearch])

async def call_agent():
    # Call the agent with a specific input
    output = Runner.run_streamed(
        starting_agent=agent,
        input="Find a real-world use case where an agentic AI is being used right now"
        )

    # Collect the result
    result_text = ""
    async for event in output.stream_events():
       if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
            result_text += event.data.delta

    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Write result to output/report.md
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(result_text)

    print(f"\n\n✓ Report saved to output/report.md")

asyncio.run(call_agent())