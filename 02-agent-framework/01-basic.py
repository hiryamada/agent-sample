import asyncio
from agent_framework.foundry import FoundryAgent
from azure.identity import AzureCliCredential
import os

agent = FoundryAgent(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=AzureCliCredential(),
    agent_name="agent1",
)


async def main():
    response = await agent.run("こんにちは！")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
