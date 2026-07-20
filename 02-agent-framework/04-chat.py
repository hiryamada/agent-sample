import asyncio
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
import os

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=AzureCliCredential(),
)
agent = Agent(
    client=client,
    name="agent",
    instructions="日本語で回答",
)

session = agent.create_session()


async def main():
    while True:
        prompt = input("ユーザー: ")
        if prompt == "exit":
            break
        result = await agent.run(prompt, session=session)
        print(f"エージェント: {result.text}")


asyncio.run(main())
