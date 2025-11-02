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
    from rich.console import Console
    console = Console()
    console.print(f"[bold blue][TOOL][/bold blue] Searching the web for: [cyan]{query}[/cyan]")
    response = tavily_client.search(f"{query}")
    return response

# =============== AGENTS ===============

# 1. Research Agent - Searches the web for information
research_agent = Agent(
    name="Research Agent",
    instructions="""
    You are a Research Agent specialized in finding ONE specific real-world use case of agentic AI.

    Your job:
    1. Perform 3-4 targeted web searches to find ONE documented company using AI agents.
    2. Use the websearch tool to search the web for the information.
    3. Make sure to Search on integration niche.
    4. For the company you find, search for:
       - Company name and specific AI agent implementation
       - The problem they had BEFORE using AI agents
       - Measurable results (numbers, percentages, cost savings)
       - Official sources (company blog, news articles, case studies)

    5. Collect concrete data:
       - How many people were doing this manually?
       - What was the cost/time before?
       - What specific results did they achieve? (e.g., "50% faster", "$2M saved")
       - What are the exact inputs and outputs of the agent?

    6. After collecting all information, hand off to the Analyst Agent by using the handoff tool

    IMPORTANT: Find ONE clear example with real numbers and official sources. Don't give generic information.
    Agentic AI use case is MUST for the report.
    After research is complete, use the handoff tool to transfer to Analyst Agent.
    """,
    model=llm_model,
    tools=[websearch],
    handoffs=[]  # Will be set after all agents are defined
)

# 2. Analyst Agent - Analyzes the research data
analyst_agent = Agent(
    name="Analyst Agent",
    instructions="""
   Your job:
    1. Receive the 5 questions and answers from Analyst Agent
    2. Write a ONE-PAGE summary using this EXACT format:

       # [Company Name]: Real-World AI Agent Use Case

       ## Question 1: What Was the Problem?

       [Write 2-3 sentences in simple language:]
       - What task was taking lots of time/money before?
       - How many people were doing this manually?
       - What was costing the company?

       **Example:** "Amazon warehouse workers were manually moving packages across the warehouse. This took 8 hours per person per day. The company needed to move packages faster without hiring more workers."

       ## Question 2: What Agent Did They Build?

       [Write 2-3 sentences answering:]
       - What does the agent do (be specific)?
       - What inputs does it get?
       - What outputs does it create?

       **Example:** "Amazon robots navigate warehouse floors using cameras and sensors. They receive instructions like 'go to shelf B-42 and pick up package #1234.' They move to that location, pick up the package, and bring it to the packing station."

       ## Question 3: How Do Humans Stay in Control?

       [Write 2-3 sentences answering:]
       - Do humans still make decisions?
       - What do humans check or approve?
       - What happens if something goes wrong?

       **Example:** "Robots follow programmed routes and safety rules. Humans monitor the robots on screens and can stop them if there's a problem. If a robot gets stuck, a human takes over and helps it."

       ## Question 4: What Results Did They Get?

       [Write 2-3 sentences answering:]
       - What improved? (speed, cost, quality, etc.)
       - By how much? (GIVE SPECIFIC NUMBERS)
       - How did this help the business?

       **Example:** "Amazon moved 50% more packages with the same number of workers. Each robot can move 300 packages per day. This saved the company millions in labor costs."

       ## Question 5: Why Did This Work?

       [Write 2-3 sentences answering:]
       - Why was this job good for an agent?
       - What made it easier/harder than other tasks?
       - Would this work for other companies?

       **Example:** "Warehouse work is repetitive — pick, move, drop. This is perfect for agents because the instructions are clear. Agents don't get tired. Any warehouse could use this."

       ## Sources

       - [Link to news article, company blog, or YouTube video]
       - [Add more sources if available]

    3. IMPORTANT RULES:
       - Use SIMPLE language (grade 10 level)
       - Keep sentences SHORT (2-3 sentences per question)
       - Include SPECIFIC NUMBERS and PERCENTAGES
       - Make it ONE PAGE total
       - Use the EXACT question format shown above

    4. Don't use complex words. Write like you're explaining to a friend.

    Your goal: A grade 10 student should easily understand this in 5 minutes.
    """,
    model=llm_model,
    tools=[],
    handoffs=[]  # Will be set after all agents are defined
)

# Set up handoffs now that all agents are defined
research_agent.handoffs = [analyst_agent]

# 4. Triage Agent - Routes the initial request
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a Triage Agent that coordinates the research workflow.

    When user asks to find agentic AI use cases:
    1. Hand off to Research Agent to gather information
    2. Research Agent will hand off to Analyst Agent
    3. Analyst Agent will create the final report

    Always start by handing off to the Research Agent.
    """,
    model=llm_model,
    handoffs=[research_agent]
)

# =============== MAIN EXECUTION ===============

async def call_agent():
    """
    Multi-Agent Research System with Streaming

    Flow:
    User → Triage Agent → Research Agent → Analyst Agent → Report
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    console = Console()

    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Multi-Agent Research System[/bold cyan]",
        border_style="cyan"
    ))
    console.print()

    # Call the research agent which will hand off to analyst then writer
    output = Runner.run_streamed(
        starting_agent=research_agent,
        input="Find ONE real-world use case where an agentic AI is being used right now with specific measurable results in E-commerce Fashion niche 2025",
        max_turns=20
    )

    # Collect the result with streaming
    result_text = ""
    console.print("[bold yellow]Generating report (streaming)...[/bold yellow]\n")
    console.print("-" * 80, style="dim")

    async for event in output.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
            result_text += event.data.delta

    console.print("\n" + "-" * 80, style="dim")

    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Write result to output/report.md
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(result_text)

    console.print()
    console.print(Panel(
        "[bold green]Report saved to output/report.md[/bold green]",
        border_style="green"
    ))
    console.print()

if __name__ == "__main__":
    asyncio.run(call_agent())