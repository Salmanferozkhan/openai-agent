# Hello Agent

A Python agent project using the OpenAI agents framework with Gemini API integration.

## Description

This project demonstrates how to create and run a simple AI agent using the `openai-agents` framework with Google's Gemini API as the underlying language model.

## Features

- Simple agent implementation using OpenAI agents framework
- Integration with Google Gemini API
- Environment variable configuration for API keys

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root with your API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. Run the agent:
   ```bash
   uv run main.py
   ```

## Dependencies

- `dotenv>=0.9.9` - Environment variable management
- `openai-agents>=0.3.1` - OpenAI agents framework

## Project Structure

```
hello_agent/
├── main.py          # Main agent implementation
├── pyproject.toml   # Project configuration and dependencies
├── README.md        # This file
└── .env             # Environment variables (create this file)
```

## Usage

The agent is configured to use Google's Gemini API and can be extended with custom instructions and capabilities as needed.
