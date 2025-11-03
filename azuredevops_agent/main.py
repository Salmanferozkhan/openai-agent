import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled,function_tool
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.release.models import ReleaseStartMetadata
from openai.types.responses import ResponseTextDeltaEvent
import pprint

load_dotenv(find_dotenv())
set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
llm_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
# ----------------------------------------------------------------------------------------------
# Fill in with your personal access token and org URL
personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
organization_url = os.getenv("ORGANIZATION_URL")
project_name = os.getenv("PROJECT_NAME")
#pprint.pprint(f"Project name: {project_name} Personal access token: {personal_access_token} Organization url: {organization_url}")
def get_azure_projectname():
    """
    Get the name of the Azure projects
    """
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    core_client = connection.clients.get_core_client()

    projects = core_client.get_projects()
    projects_list = []

    for project in projects:
        projects_list.append(project.name)

    return projects_list

@function_tool
def get_release_definitions():
    """
    Get all release definitions for the Azure DevOps project. Returns a list of dictionaries with 'id' and 'name' fields.
    Use this tool first to get the list of all available release definitions and their IDs.
    """

    print(f"TOOL CALLING - Getting release definitions for project {project_name}")
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
    pprint.pprint(f"Found {len(releases_list)} release definitions")
    return releases_list

@function_tool
def create_release(definition_id:int, description:str="Release triggered via API", is_draft:bool=False, reason:str="manual"):
    """
    Create a new release from a release definition.
    Args:
        definition_id: The ID of the release definition to create a release from
        description: Description for the release
        is_draft: Whether this is a draft release
        reason: Reason for creating the release
    """
    pprint.pprint(f"TOOL CALLING - Creating release for project {project_name} with definition id {definition_id}")
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
    pprint.pprint(f"Release created: {release.name}")
    return {
        'id': release.id,
        'name': release.name,
        'status': release.status,
        'created_on': str(release.created_on)
    }

instructions="""
You are a helpful assistant that manages Azure DevOps releases.

When the user asks to create a release:
1. ALWAYS start by calling get_release_definitions() to get all available release definitions
2. Search through the results to find a release definition name that matches what the user requested
3. Extract the 'id' field from the matching release definition
4. Call create_release with that definition_id to create the release

IMPORTANT: You must call get_release_definitions first, even if the user provides a release name.
"""
agent:Agent = Agent(name="Azure DevOps", instructions=instructions, model=llm_model, tools=[get_release_definitions, create_release])

async def run_agent_with_streaming():
    """
    Run the Azure DevOps agent with streaming output
    """
    print("\n" + "="*80)
    print("Azure DevOps Release Agent - Streaming Mode")
    print("="*80 + "\n")

    output = Runner.run_streamed(
        starting_agent=agent,
        input="Create a release for test project",
        max_turns=10
    )

    result_text = ""
    print("Agent Response (streaming):")
    print("-" * 80)

    async for event in output.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
            result_text += event.data.delta

    print("\n" + "-" * 80)
    print("\nFinal Output:")
    print(result_text)
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(run_agent_with_streaming())

