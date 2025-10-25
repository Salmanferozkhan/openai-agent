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

# =============== TOOLS ===============

@function_tool
def websearch(query:str):
    """
    Search the web for the query
    """
    print(f"[TOOL] Searching the web for: {query}")
    response = tavily_client.search(f"{query}")
    return response

# =============== AGENTS ===============

# 1. Research Agent - Searches the web for information
research_agent = Agent(
    name="Research Agent",
    instructions="""
    You are a Research Agent specialized in finding real-world use cases of agentic AI.

    Your job:
    1. Perform 3-4 different web searches to gather comprehensive information about agentic AI use cases
    2. Search for:
       - Companies using AI agents in production
       - Real-world implementations with measurable results
       - Different industries (warehouse, customer service, fraud detection, etc.)
       - Recent news and case studies
    3. Collect raw data from multiple sources
    4. Hand off all your findings to the Analyst Agent for analysis

    Be thorough and search from multiple angles. Don't analyze yet - just gather information.
    """,
    model=llm_model,
    tools=[websearch]
)

# 2. Analyst Agent - Analyzes the research data
analyst_agent = Agent(
    name="Analyst Agent",
    instructions="""
    You are an Analyst Agent specialized in analyzing agentic AI use cases.

    Your job:
    1. Receive research data from the Research Agent
    2. Pick the BEST real-world use case from the data
    3. Extract and structure key information:
       - Company name and problem
       - What the agent does (inputs/outputs)
       - Human oversight mechanisms
       - Measurable results (numbers, percentages)
       - Why it worked
    4. Verify facts and ensure data quality
    5. Hand off structured findings to the Writer Agent

    Focus on finding concrete numbers and measurable impacts. Choose a use case with clear, verifiable results.
    """,
    model=llm_model,
    tools=[]
)

# 3. Writer Agent - Writes the final report
writer_agent = Agent(
    name="Writer Agent",
    instructions="""
    You are a Writer Agent specialized in creating clear, simple reports.

    Your job:
    1. Receive structured findings from the Analyst Agent
    2. Write a comprehensive report in Grade 10 level language
    3. Use this EXACT structure:

       # [Company Name]: Real-World AI Agent Implementation

       ## 1. The Problem They Faced
       [Clear explanation of the problem, costs, and manual effort]

       ## 2. The AI Agent Solution
       ### What the Agent Does:
       - Input: [what data/instructions it receives]
       - Process: [what it does]
       - Output: [what results it creates]

       ### Human Oversight:
       [How humans stay in control and what they monitor]

       ## 3. Measurable Results
       [Specific numbers, percentages, and improvements]

       ## 4. Why This Worked
       [Analysis of why AI was suited for this task]

       ## 5. Sources
       [Links to sources]

    4. Use simple language, bullet points, and clear formatting
    5. Include ALL specific numbers and percentages from the analysis

    Write clearly and concisely. Make it easy to understand for a grade 10 student.
    """,
    model=llm_model,
    tools=[]
)

# 4. Triage Agent - Routes the initial request
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a Triage Agent that coordinates the research workflow.

    When user asks to find agentic AI use cases:
    1. Hand off to Research Agent to gather information
    2. Research Agent will hand off to Analyst Agent
    3. Analyst Agent will hand off to Writer Agent
    4. Writer Agent will create the final report

    Always start by handing off to the Research Agent.
    """,
    model=llm_model,
    handoffs=[research_agent, analyst_agent, writer_agent]
)

# =============== MAIN EXECUTION ===============

async def call_agent():
    """
    Multi-Agent Research System with Streaming

    Flow:
    User → Triage Agent → Research Agent → Analyst Agent → Writer Agent → Report
    """
    print("\n" + "="*80)
    print("🤖 Multi-Agent Research System")
    print("="*80 + "\n")

    # Call the triage agent which will coordinate all other agents
    output = Runner.run_streamed(
        starting_agent=triage_agent,
        input="Find a real-world use case where an agentic AI is being used right now"
    )

    # Collect the result with streaming
    result_text = ""
    print("📝 Generating report (streaming)...\n")
    print("-" * 80)

    async for event in output.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
            result_text += event.data.delta

    print("\n" + "-" * 80)

    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Write result to output/report.md
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(result_text)

    print(f"\n✓ Report saved to output/report.md")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(call_agent())