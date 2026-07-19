import gradio as gr

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


async def stream_chat(user_prompt, _):
    response_text = ""
    async for delta in await agent.run(user_prompt, stream=True, session=session):
        response_text += delta.text
        yield response_text


gr.ChatInterface(fn=stream_chat).launch()
