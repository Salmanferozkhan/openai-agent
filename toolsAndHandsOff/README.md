# Tools and Handoffs Agent

A simple demonstration of OpenAI Agents SDK using Google's Gemini model as the LLM provider.

## Prerequisites

- Python 3.13+
- UV package manager
- Google Gemini API key

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Running

```bash
uv run python toolsAndHandsOff/main.py
```

## Project Structure

- `main.py` - Main entry point demonstrating agent creation with Gemini integration
- `.env` - Environment variables (not tracked in git)
- `pyproject.toml` - Project dependencies
