import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.release.models import ReleaseStartMetadata

load_dotenv(find_dotenv())
set_tracing_disabled(True)

# Configuration
personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
organization_url = os.getenv("ORGANIZATION_URL")
project_name = os.getenv("PROJECT_NAME")

# Setup LLM
external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
llm_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)


# Azure DevOps Functions
@function_tool
def get_release_definitions():
    """
    Get all release definitions for the Azure DevOps project. Returns a list of dictionaries with 'id' and 'name' fields.
    Use this tool first to get the list of all available release definitions and their IDs.
    """
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    release_client = connection.clients.get_release_client()

    release_definitions = release_client.get_release_definitions(project=project_name)

    releases_list = []
    for release_def in release_definitions:
        releases_list.append({
            'id': release_def.id,
            'name': release_def.name
        })
    return releases_list


@function_tool
def create_release(definition_id: int, description: str = "Release triggered via UI", is_draft: bool = False, reason: str = "manual"):
    """
    Create a new release from a release definition.
    Args:
        definition_id: The ID of the release definition to create a release from
        description: Description for the release
        is_draft: Whether this is a draft release
        reason: Reason for creating the release
    """
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    release_client = connection.clients.get_release_client()

    release_metadata = ReleaseStartMetadata(
        definition_id=definition_id,
        description=description,
        is_draft=is_draft,
        reason=reason
    )

    release = release_client.create_release(
        release_start_metadata=release_metadata,
        project=project_name
    )

    return {
        'id': release.id,
        'name': release.name,
        'status': release.status,
        'created_on': str(release.created_on)
    }


# Agent instructions
instructions = """
You are a helpful assistant that manages Azure DevOps releases.

When the user asks to create a release:
1. ALWAYS start by calling get_release_definitions() to get all available release definitions
2. Search through the results to find a release definition name that matches what the user requested
3. Extract the 'id' field from the matching release definition
4. Call create_release with that definition_id to create the release

When the user asks to list releases or release definitions:
1. Call get_release_definitions() to get all release definitions
2. Present them in a clear, organized format

IMPORTANT: You must call get_release_definitions first, even if the user provides a release name.
"""


@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    # Create agent
    agent = Agent(
        name="Azure DevOps Agent",
        instructions=instructions,
        model=llm_model,
        tools=[get_release_definitions, create_release]
    )

    # Store agent in session
    cl.user_session.set("agent", agent)

    # Welcome message
    await cl.Message(
        content=f"""👋 Welcome to Azure DevOps Release Manager!

**Project**: {project_name}

I can help you with:
- 📋 List all release definitions
- 🚀 Create releases from release definitions
- 🔍 Find specific release definitions

**Examples:**
- "List all release definitions"
- "Create a release for backend-api-production"
- "Show me release definitions for production"

How can I help you today?"""
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    # Get agent from session
    agent = cl.user_session.get("agent")

    # Show loading message
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Run the agent
        result = Runner.run_sync(agent, message.content)

        # Update message with result
        msg.content = result.final_output
        await msg.update()

    except Exception as e:
        # Handle errors
        msg.content = f"❌ Error: {str(e)}\n\nPlease make sure your Azure DevOps credentials are configured correctly in the `.env` file."
        await msg.update()
