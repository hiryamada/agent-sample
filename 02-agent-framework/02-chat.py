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
session = agent.create_session()


async def main():
    while True:
        prompt = await asyncio.to_thread(input, "ユーザー: ")
        if prompt == "exit":
            break

        print("エージェント: ", end="", flush=True)

        async for delta in await agent.run(prompt, stream=True, session=session):
            print(delta, end="", flush=True)

        print()


if __name__ == "__main__":
    asyncio.run(main())
