# Azure DevOps Agent

An intelligent agent that interacts with Azure DevOps APIs to manage releases automatically using the Azure DevOps Python SDK.

## Features

- **Get Projects**: Retrieve all Azure DevOps projects from your organization
- **Get Release Definitions**: List all release definitions for a specific project
- **Create Releases**: Automatically create releases from release definitions by name
- **Real-time Streaming**: See agent responses in real-time as they're generated
- **Chainlit UI**: Beautiful web interface for natural language interactions
- **Async Support**: Fully asynchronous implementation for better performance

## Prerequisites

- Python 3.8+
- Azure DevOps organization
- Personal Access Token (PAT) with appropriate permissions

## Installation

```bash
uv sync
```

## Configuration

Create a `.env` file in the project directory with the following variables:

```env
PERSONAL_ACCESS_TOKEN=your_azure_devops_pat
ORGANIZATION_URL=https://dev.azure.com/YourOrganization
PROJECT_NAME=YourProjectName
GEMINI_API_KEY=your_gemini_api_key
```

### Getting a Personal Access Token

1. Go to Azure DevOps
2. Click on User Settings > Personal Access Tokens
3. Create a new token with the following scopes:
   - **Release**: Read, write, & execute
   - **Project and Team**: Read

## Usage

### Option 1: Chainlit Web UI (Recommended)

Run the interactive web interface:

```bash
uv run chainlit run app.py -w
```

Then open your browser at `http://localhost:8000`

The Chainlit UI provides:
- 💬 Interactive chat interface
- 🎯 Natural language commands
- 📊 Real-time streaming responses
- 🎨 Beautiful, user-friendly interface
- ⚡ Live updates as the agent thinks and responds

**Example commands to try:**
- "List all release definitions"
- "Create a release for backend-api-production"
- "Show me all production releases"

### Option 2: Command Line with Streaming (main.py)

Run the agent directly from the command line with real-time streaming output:

```bash
uv run python main.py
```

Features:
- 🔄 Real-time streaming responses
- 📝 See agent thinking process live
- 💾 Saves final output for review

### Option 3: Python Script

```python
from main import get_azure_projectname, get_release_definitions, create_release

# Get all projects
projects = get_azure_projectname()
print(projects)

# Get release definitions for a project
definitions = get_release_definitions()
print(definitions)

# Create a release
release = create_release(definition_id=12)
print(release)
```

### Using the Agent with Streaming

The agent can automatically find and create releases based on natural language requests with real-time streaming:

```python
import asyncio
from agents import Agent, Runner
from main import get_release_definitions, create_release, llm_model
from openai.types.responses import ResponseTextDeltaEvent

agent = Agent(
    name="Azure DevOps",
    instructions="""
    You are a helpful assistant that manages Azure DevOps releases.

    When the user asks to create a release:
    1. ALWAYS start by calling get_release_definitions() to get all available release definitions
    2. Search through the results to find a release definition name that matches what the user requested
    3. Extract the 'id' field from the matching release definition
    4. Call create_release with that definition_id to create the release
    """,
    model=llm_model,
    tools=[get_release_definitions, create_release]
)

async def run_with_streaming():
    output = Runner.run_streamed(
        starting_agent=agent,
        input="Create a release for backend-api-production",
        max_turns=10
    )

    async for event in output.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(run_with_streaming())
```

## API Reference

### Functions

#### `get_azure_projectname()`
Returns a list of all project names in your Azure DevOps organization.

**Returns**: `List[str]`

#### `get_release_definitions()`
Gets all release definitions for the configured project.

**Returns**: `List[Dict[str, Any]]` - List of dictionaries with `id` and `name` fields

#### `create_release(definition_id, description, is_draft, reason)`
Creates a new release from a release definition.

**Parameters**:
- `definition_id` (int): The ID of the release definition
- `description` (str, optional): Description for the release. Default: "Release triggered via API"
- `is_draft` (bool, optional): Whether this is a draft release. Default: False
- `reason` (str, optional): Reason for creating the release. Default: "manual"

**Returns**: `Dict[str, Any]` - Dictionary with release details (id, name, status, created_on)

## Azure DevOps SDK Methods Used

This project uses the following Azure DevOps Python SDK methods:

| Function | SDK Method | REST API Endpoint |
|----------|------------|-------------------|
| `get_azure_projectname()` | `core_client.get_projects()` | `GET https://dev.azure.com/{organization}/_apis/core/projects` |
| `get_release_definitions()` | `release_client.get_release_definitions(project)` | `GET https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions` |
| `create_release()` | `release_client.create_release(release_start_metadata, project)` | `POST https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases` |

## Example Output

### CLI Streaming Output:
```bash
================================================================================
Azure DevOps Release Agent - Streaming Mode
================================================================================

Agent Response (streaming):
--------------------------------------------------------------------------------
I'll help you create a release for the test project. Let me first get all available release definitions...

[Agent retrieves definitions in real-time]

Found 45 release definitions. Looking for 'test project'...

Creating release for definition ID 12...

Successfully created Release-3 for backend-api-production!
--------------------------------------------------------------------------------

Final Output:
I have created a release for `backend-api-production` with the name `Release-3`.

================================================================================
```

### Chainlit UI:
The web interface shows the same streaming output in a beautiful chat interface with real-time updates.

## Project Structure

```
azuredevops_agent/
├── app.py               # Chainlit web UI application
├── main.py              # CLI application with agent and tools
├── .env                 # Environment variables (not committed)
├── pyproject.toml       # Project dependencies
├── .chainlit/           # Chainlit configuration (auto-generated)
└── README.md           # This file
```

## License

MIT
