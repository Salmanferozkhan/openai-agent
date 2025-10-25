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


# =============== TOOLS ===============

@function_tool
def get_release_definitions():
    """
    Get all release definitions for the Azure DevOps project. Returns a list of dictionaries with 'id' and 'name' fields.
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
    Deploy/Create a new release from a release definition ID.
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


# =============== AGENTS ===============

# List Agent - Lists all release definitions
list_agent = Agent(
    name="List Agent",
    instructions="""
    You are a List Agent specialized in showing release definitions.

    Your job:
    1. Call get_release_definitions() to get all release definitions
    2. Present them in a clear, organized format with their IDs and names with beautiful table format
    3. Tell the user they can ask to deploy any of these releases

    Format the output nicely with bullet points or numbers. Keep it organized.

    Keep it simple and fast. Don't format with markdown or bullets - just numbered list.
    """,
    model=llm_model,
    tools=[get_release_definitions]
)

# Deploy Agent - Deploys a specific release
deploy_agent = Agent(
    name="Deploy Agent",
    instructions="""
    You are a Deploy Agent specialized in deploying releases.

    Your job:
    1. Call get_release_definitions() to get all available releases
    2. Find the release definition that matches the user's request (by name or partial name match or ID)
    3. Extract the definition ID
    4. Call create_release with that definition_id to deploy it IMMEDIATELY
    5. Confirm the deployment was successful with full details (ID, name, status, created time)

    Deploy immediately when you find a match. Be precise about which release was deployed.
    """,
    model=llm_model,
    tools=[get_release_definitions, create_release]
)

# Triage Agent - Routes to appropriate agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a Triage Agent that routes user requests to the appropriate specialist agent.

    Analyze the user's request and hand off to:
    - **List Agent**: If user wants to see/list all releases, release definitions, or available releases
    - **Deploy Agent**: If user wants to deploy, create, or trigger a release

    Keywords for List Agent: "list", "show", "display", "get", "what are", "available", "all releases"
    Keywords for Deploy Agent: "deploy", "create", "trigger", "release", "start", "run"

    Always hand off to the appropriate agent based on the user's intent.
    """,
    model=llm_model,
    handoffs=[list_agent, deploy_agent]
)


@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    # Store triage agent in session
    cl.user_session.set("agent", triage_agent)

    # Welcome message
    await cl.Message(
        content=f"""Welcome to Azure DevOps Release Manager with Handoff Agents!

**Project**: {project_name}

I use specialized agents to help you:
- **List Agent**: Lists all available release definitions
- **Deploy Agent**: Deploys releases to your environments

**Try these commands:**
- "Show me all releases" or "List all release definitions"
- "Deploy the cirbasolutions release" or "Create release for ID 264"

How can I help you today?"""
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    # Get agent from session
    agent = cl.user_session.get("agent")

    # Create a message with loading indicator
    msg = cl.Message(content="")

    try:
        # Show step with loading indicator
        async with cl.Step(name="Processing your request", type="tool") as step:
            step.output = "Analyzing your request and routing to the appropriate agent..."

            # Run the agent with handoff support
            result = Runner.run_sync(agent, message.content)

            step.output = "Request processed successfully!"

        # Send the final result
        msg.content = result.final_output
        await msg.send()

    except Exception as e:
        # Handle errors
        msg.content = f"Error: {str(e)}\n\nPlease make sure your Azure DevOps credentials are configured correctly in the `.env` file."
        await msg.send()
