from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
import os
from agent_framework import create_harness_agent
import asyncio

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=AzureCliCredential(),
)

agent = create_harness_agent(
    client=client,
    agent_instructions="日本語で回答, ツールを使用する際はツールの名前、引数、目的、得られた結果を簡単に説明しながら使用",
)

session = agent.create_session()


async def main():
    while True:
        prompt = input("ユーザー: ")
        response = await agent.run(prompt, session=session)
        print(f"エージェント: {response.text}")


asyncio.run(main())
