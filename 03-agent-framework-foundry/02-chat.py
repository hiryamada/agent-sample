import asyncio
from agent_framework.foundry import FoundryAgent
from azure.identity import AzureCliCredential
import os


agent = FoundryAgent(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=AzureCliCredential(),
    agent_name="agent1",
)


# create Agent Framework lightweight session (on memory)
# session = agent.create_session()


async def main():
    # create a "conversation" on the agent (persisted)
    session = await agent.create_conversation()
    while True:
        prompt = await asyncio.to_thread(input, "ユーザー: ")
        if prompt == "exit":
            break

        print("エージェント: ", end="", flush=True)

        async for delta in await agent.run(prompt, stream=True, session=session):
            print(delta, end="", flush=True)

        print()


asyncio.run(main())
