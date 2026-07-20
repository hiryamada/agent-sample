import asyncio
from agent_framework import Agent, Content, Message, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
import os

from pydantic import Field
from typing import Annotated
from random import randint


@tool(approval_mode="always_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    result = f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."
    print(f"Tool: get_weather({location}) -> {result}")
    return result


client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=AzureCliCredential(),
)
agent = Agent(
    client=client, name="agent2", instructions="日本語で回答", tools=[get_weather]
)

session = agent.create_session()


async def approve_function_call(func_call: Content) -> bool:
    print("関数呼び出し:")
    print(f"- 関数名: {func_call.name}")
    print(f"- 引数: {func_call.arguments}")
    yesno = await asyncio.to_thread(input, "- この関数呼び出しを実行しますか？ (y/n): ")
    return yesno.lower() == "y"


async def main():
    prompt = "こんにちは！東京と大阪の天気は？"
    print(f"ユーザー: {prompt}")
    result = await agent.run(prompt, session=session)
    if result.user_input_requests:
        messages: list[Message] = []
        for request in result.user_input_requests:
            if (func_call := request.function_call) is None:
                continue
            approved = await approve_function_call(func_call)
            message = Message(
                role="user",
                contents=[request.to_function_approval_response(approved=approved)],
            )
            messages.append(message)
        final_result = await agent.run(messages, session=session)
        print(f"エージェント: {final_result.text}")

    else:
        print(f"エージェント: {result.text}")


asyncio.run(main())
