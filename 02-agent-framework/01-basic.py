import asyncio
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential
import os

client = FoundryChatClient(
    credential=AzureCliCredential(),
    model=os.environ["FOUNDRY_MODEL"],
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
)
agent = client.as_agent(name="agent1")


async def main():
    response = await agent.run("こんにちは！")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
