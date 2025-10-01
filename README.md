# OpenAI Agents SDK - Fundamentals of Agentic AI

A collection of AI agents built using the OpenAI Agents SDK, demonstrating fundamental concepts of agentic AI systems.

## Project Structure

This repository contains multiple agent implementations, each showcasing different capabilities:

### 🤖 [Hello Agent](./hello_agent/)
A basic agent implementation that demonstrates the fundamentals of creating an AI agent.
- Simple agent setup and configuration
- Basic conversation capabilities
- Foundation for understanding agent architecture

### 🔍 [WebSearch Agent](./websearch_agent/)
An intelligent web search agent that can search the internet and provide comprehensive responses.
- Web search functionality using Tavily API
- Integration with Gemini 2.5 Flash model
- Real-time information retrieval and processing

### ⚙️ [Agent Configurations](./agent_configurations/)
Examples and configurations for different agent setups.
- Agent-level configurations
- Global-level settings
- Run-level parameters

### 🚀 [Azure DevOps Agent](./azuredevops_agent/)
An intelligent agent that manages Azure DevOps releases automatically.
- Retrieve projects and release definitions
- Create releases from release definitions by name
- Integration with Azure DevOps Python SDK
- Natural language release management

## Prerequisites

- Python 3.13 or higher
- OpenAI Agents SDK
- API keys for respective services (Gemini, Tavily, etc.)

## Quick Start

1. Clone this repository:
```bash
git clone https://github.com/Salmanferozkhan/openai-agent.git
cd openai-agent
```

2. Navigate to the specific agent directory you want to explore:
```bash
cd hello_agent
# or
cd websearch_agent
# or
cd azuredevops_agent
```

3. Install dependencies:
```bash
uv sync
```

4. Set up environment variables by creating a `.env` file with your API keys.

5. Run the agent:
```bash
python main.py
```

## Features

- **Multiple Agent Types**: Different agents for various use cases
- **Modular Architecture**: Each agent is self-contained with its own dependencies
- **Easy Configuration**: Simple setup with environment variables
- **Real-world Examples**: Practical implementations you can build upon

## Learning Path

1. **Start with Hello Agent** - Understand basic agent concepts
2. **Explore WebSearch Agent** - Learn about tool integration and external APIs
3. **Review Agent Configurations** - Understand different configuration patterns
4. **Try Azure DevOps Agent** - Learn how to integrate with enterprise APIs and manage complex workflows

## Technologies Used

- **OpenAI Agents SDK** - Core agent framework
- **Gemini 2.5 Flash** - Language model
- **Tavily API** - Web search functionality
- **Azure DevOps Python SDK** - Azure DevOps integration
- **Python 3.13** - Programming language
- **UV** - Package management

## Contributing

Feel free to contribute by:
- Adding new agent implementations
- Improving existing agents
- Adding documentation
- Reporting issues

## License

This project is for educational purposes, demonstrating the fundamentals of agentic AI systems.

---

## Individual Agent Documentation

Each agent directory contains its own detailed README with specific setup instructions, usage examples, and implementation details. Please refer to the individual README files for more information.