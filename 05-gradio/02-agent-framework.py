import gradio as gr

from agent_framework.foundry import FoundryAgent
from azure.identity import AzureCliCredential
import os

agent = FoundryAgent(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=AzureCliCredential(),
    agent_name="agent1",
)

session = agent.create_session()


async def stream_chat(user_prompt, _):
    response_text = ""
    async for delta in await agent.run(user_prompt, stream=True, session=session):
        response_text += delta.text
        yield response_text


gr.ChatInterface(fn=stream_chat).launch()
