# Azure DevOps Agent

An intelligent agent that interacts with Azure DevOps APIs to manage releases automatically using the Azure DevOps Python SDK.

## Features

- **Get Projects**: Retrieve all Azure DevOps projects from your organization
- **Get Release Definitions**: List all release definitions for a specific project
- **Create Releases**: Automatically create releases from release definitions by name

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

### Basic Example

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

### Using the Agent

The agent can automatically find and create releases based on natural language requests:

```python
from agents import Agent, Runner
from main import get_release_definitions, create_release, llm_model

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

result = Runner.run_sync(
    agent,
    "Create a release for backend-api-production"
)
print(result.final_output)
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

```bash
Project name: MyDevOpsProject
TOOL CALLING - Getting release definitions for project MyDevOpsProject
Found 45 release definitions
TOOL CALLING - Creating release for project MyDevOpsProject with definition id 12
Release created: Release-3
I have created a release for `backend-api-production` with the name `Release-3`.
```

## Project Structure

```
azuredevops_agent/
├── main.py              # Main application with agent and tools
├── .env                 # Environment variables (not committed)
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```

## License

MIT
