# Research Agent - Multi-Agent System

A **multi-agent AI system** that finds and analyzes real-world use cases of agentic AI implementations. The system uses specialized agents working together with **handoff patterns** and **streaming output**.

## Architecture

This project demonstrates a **4-agent architecture** with handoffs:

```
User Request
    ↓
🎯 Triage Agent (Coordinator)
    ↓
🔍 Research Agent (Searcher) → Performs 3-4 web searches
    ↓
📊 Analyst Agent (Analyzer) → Extracts and structures data
    ↓
✍️ Writer Agent (Reporter) → Creates final report
    ↓
📄 Saved to output/report.md
```

### Agent Roles:

1. **Triage Agent** - Routes requests and coordinates workflow
2. **Research Agent** - Searches web for real-world AI agent use cases
3. **Analyst Agent** - Analyzes data, extracts key insights and numbers
4. **Writer Agent** - Creates structured, Grade 10-level reports

## Features

- 🔄 **Multi-Agent Handoffs** - Agents pass work to specialized agents
- 🔍 **Parallel Web Searches** - Research agent performs multiple searches
- 🤖 **Gemini 2.5 Flash Model** - Powered by Google's advanced language model
- 📊 **Structured Analysis** - Analyst verifies facts and finds concrete numbers
- 🌊 **Streaming Output** - Real-time streaming of final report generation
- 📝 **Automatic Report Generation** - Saves research findings to markdown files

## Why Multi-Agent?

**Single Agent Problems:**
- One agent handles everything (search + analysis + writing)
- Sequential processing - slower
- If one step fails, everything fails

**Multi-Agent Benefits:**
- ✅ Each agent specialized in one task
- ✅ Better quality output
- ✅ Research agent can perform parallel searches
- ✅ Analyst ensures data quality
- ✅ Writer focuses only on clear communication
- ✅ Error recovery at each stage

## Streaming Support

This system demonstrates **streaming capabilities** where you can see the AI's response being generated in real-time, character by character. This provides:
- Immediate feedback to users
- Better user experience for long-running tasks
- Ability to monitor the agent's thinking process

The streaming is implemented using:
```python
async for event in output.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        print(event.data.delta, end="", flush=True)
```

## Prerequisites

- Python 3.13+
- UV package manager
- Google Gemini API key
- Tavily API key

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Running

```bash
uv run python main.py
```

The multi-agent system will:
1. **Triage Agent** - Receives your request and routes to Research Agent
2. **Research Agent** - Performs 3-4 web searches for agentic AI use cases
3. **Analyst Agent** - Analyzes findings, extracts numbers and key insights
4. **Writer Agent** - Creates final report with streaming output
5. **Save** - Report saved to `output/report.md`

## Agent Workflow Example

```
User: "Find a real-world use case where an agentic AI is being used"
   ↓
Triage Agent: "Routing to Research Agent..."
   ↓
Research Agent:
   - Search 1: "companies using AI agents 2025"
   - Search 2: "agentic AI warehouse automation"
   - Search 3: "AI agents customer service results"
   - Search 4: "real world AI agent implementations"
   → Hands off data to Analyst Agent
   ↓
Analyst Agent:
   - Picks best use case from search results
   - Extracts company name, problem, solution, results
   - Verifies concrete numbers (e.g., "30% cost reduction")
   → Hands off structured data to Writer Agent
   ↓
Writer Agent:
   - Creates markdown report (streaming to console)
   - Uses Grade 10 level language
   - Includes all sources
   → Final output saved
```

## Report Structure

The generated report includes:

1. **The Problem They Faced**
   - Company name
   - Problem description
   - Manual costs and effort

2. **The AI Agent Solution**
   - What the agent does (inputs/outputs)
   - Human oversight mechanisms

3. **Measurable Results**
   - Specific numbers and percentages
   - Business impact

4. **Why This Worked**
   - Why AI was suited for this task
   - Applicability to other industries

5. **Sources**
   - Links and references

## Output

Research reports are automatically saved to the `output/` directory as markdown files.

## Technologies Used

- **OpenAI Agents SDK** - Multi-agent framework with handoffs and streaming
- **Gemini 2.5 Flash** - Language model
- **Tavily Python SDK** - Web search API
- **Rich** - Terminal formatting
- **AsyncIO** - Asynchronous streaming support

## Learning Points

This project demonstrates:
- **Handoff Pattern** - How agents transfer work to specialized agents
- **Separation of Concerns** - Each agent has one clear responsibility
- **Streaming** - Real-time output generation
- **Agent Coordination** - How multiple agents work together
- **Tool Usage** - Only Research Agent has websearch tool
