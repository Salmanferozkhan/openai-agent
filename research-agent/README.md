# Research Agent

An AI research agent that finds and analyzes real-world use cases of agentic AI implementations. The agent uses web search capabilities to gather information and generates comprehensive reports with **streaming output**.

## Features

- = **Web Search Integration** - Uses Tavily API for real-time web searches
- > **Gemini 2.5 Flash Model** - Powered by Google's advanced language model
- =Ê **Structured Research** - Generates detailed reports with specific sections
- <
 **Streaming Output** - Real-time streaming of agent responses as they're generated
- =Ý **Automatic Report Generation** - Saves research findings to markdown files

## Streaming Support

This agent demonstrates **streaming capabilities** where you can see the AI's response being generated in real-time, character by character. This provides:
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

The agent will:
1. Search for real-world agentic AI use cases
2. Stream the response to the console in real-time
3. Analyze and structure the findings
4. Generate a comprehensive report
5. Save the report to `output/report.md`

## Report Structure

The generated report includes:

1. **Company Overview**
   - Company name
   - Problem faced

2. **Agent Implementation**
   - What the agent does
   - Human oversight and control

3. **Results & Impact**
   - Measurable improvements
   - Business benefits

4. **Analysis**
   - Why this solution worked
   - Applicability to other industries

5. **Sources**
   - Links and references

## Output

Research reports are automatically saved to the `output/` directory as markdown files.

## Technologies Used

- **OpenAI Agents SDK** - Agent framework with streaming support
- **Gemini 2.5 Flash** - Language model
- **Tavily Python SDK** - Web search API
- **Rich** - Terminal formatting
- **AsyncIO** - Asynchronous streaming support
