import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.release.models import ReleaseStartMetadata
import pprint

load_dotenv(find_dotenv())
set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
llm_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

# Configuration
personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
organization_url = os.getenv("ORGANIZATION_URL")
project_name = os.getenv("PROJECT_NAME")

# Global variable to store releases for context
current_releases = []

# =============== TOOLS ===============

@function_tool
def get_release_definitions():
    """
    Get all release definitions for the Azure DevOps project. Returns a list of dictionaries with 'id' and 'name' fields.
    """
    global current_releases

    print(f"Getting release definitions for project {project_name}")
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

    current_releases = releases_list
    print(f"Found {len(releases_list)} release definitions")
    return releases_list

@function_tool
def create_release(definition_id: int, description: str = "Release triggered via handoff agent", is_draft: bool = False, reason: str = "manual"):
    """
    Deploy/Create a new release from a release definition ID.
    """
    print(f"Deploying release for project {project_name} with definition id {definition_id}")
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
    print(f"Release deployed: {release.name}")
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
    2. Present them in a clear, organized format with their IDs and names
    3. Tell the user they can ask to deploy any of these releases

    Format the output nicely with numbers or bullet points.
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
    1. First, call get_release_definitions() to get all available releases
    2. Find the release definition that matches the user's request (by name or ID)
    3. Extract the definition ID
    4. Call create_release with that definition_id to deploy it
    5. Confirm the deployment was successful

    Be precise and always confirm which release you're deploying before doing it.
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

    Keywords for List Agent: "list", "show", "display", "get", "what are", "available"
    Keywords for Deploy Agent: "deploy", "create", "trigger", "release", "start"

    Always hand off to the appropriate agent based on the user's intent.
    """,
    model=llm_model,
    handoffs=[list_agent, deploy_agent]
)

# =============== MAIN ===============

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Azure DevOps Handoff Agent System")
    print(f"Project: {project_name}")
    print("="*60 + "\n")

    # Test 1: List releases
    print("\n--- Test 1: Listing Releases ---")
    result1 = Runner.run_sync(triage_agent, "Show me all available releases")
    print(f"\nResult:\n{result1.final_output}\n")

    # Test 2: Deploy a release
    print("\n--- Test 2: Deploying a Release ---")
    result2 = Runner.run_sync(triage_agent, "Deploy the backend-api-production release")
    print(f"\nResult:\n{result2.final_output}\n")