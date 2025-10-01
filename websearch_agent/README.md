# WebSearch Agent

A simple AI agent that can search the web using the Tavily search API and provide intelligent responses based on current web information.

## Features

- Web search functionality using Tavily API
- Integration with Gemini 2.5 Flash model via OpenAI-compatible API
- Asynchronous operation support
- Simple function tool for web searching

## Prerequisites

- Python 3.13 or higher
- OpenAI Agents SDK
- Tavily API key
- Gemini API key

## Installation

1. Install dependencies:
```bash
uv sync
```

2. Create a `.env` file in the project root with your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage

Run the agent:
```bash
python main.py
```

The default example searches for "News of Agentic AI 2025" and returns relevant web results.

## Code Structure

- `main.py` - Main application file containing the agent setup and execution
- `pyproject.toml` - Project dependencies and configuration
- `.env` - Environment variables for API keys (create this file)

## How it Works

1. The agent uses Gemini 2.5 Flash model through an OpenAI-compatible API endpoint
2. Web search functionality is provided by the Tavily search API
3. The `websearch` function tool allows the agent to search the web for any query
4. Results are processed and returned as intelligent responses

## Dependencies

- `openai-agents>=0.3.2` - AI agent framework
- `tavily-python>=0.7.12` - Web search API client
- `dotenv>=0.9.9` - Environment variable management

## Example Output

The agent will search for the specified query and return structured information from the web, including relevant articles, news, and other content related to the search term.