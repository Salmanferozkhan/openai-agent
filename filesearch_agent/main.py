import os
import re
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, FileSearchTool

load_dotenv(find_dotenv())

agent = Agent(name="Assistant", instructions="""
You are a helpful assistant that can search the file system and return the results
You are a Shopify developer and you are given a task to generate a sample request for product create graphql mutation of shopify using file search tool
You have to use the file search tool to search the file system and return the results
DO NOT include any other text in your response other than the request
ONLY include the GRAPHQL request in your response
Make sure only return one mutation per entity
Start your response with the entity name like: ENTITY: productCreate
Then provide the GraphQL request
""",
              model="gpt-5-nano",
              tools=[FileSearchTool(
                max_num_results=3,
                vector_store_ids=["vs_68f4ae390f008191a13ee093a7203adb"]
              )])

result = Runner.run_sync(agent, 
"""
generate me a sample request for product create 
& product update graphql & order create & order update graphql mutation of shopify using file search tool
""")

output = result.final_output

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Parse entities and save to separate files
entities = output.split("ENTITY:")
for entity_content in entities:
    entity_content = entity_content.strip()
    if not entity_content:
        continue

    # Extract entity name from first line
    lines = entity_content.split("\n", 1)
    entity_name = lines[0].strip()
    graphql_content = lines[1] if len(lines) > 1 else ""

    # Clean entity name for filename
    filename = re.sub(r'[^\w\s-]', '', entity_name).strip().replace(' ', '_')

    # Save to file
    filepath = os.path.join("output", f"{filename}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(graphql_content.strip())

    print(f"Saved {filename}.md")

print("\nAll files saved to output folder")