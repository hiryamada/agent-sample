import gradio as gr
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
import os

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
openai = AIProjectClient(
    endpoint=endpoint, credential=AzureCliCredential()
).get_openai_client()
conversation = openai.conversations.create()


def stream_chat(user_prompt, _):
    response_text = ""
    with openai.responses.stream(
        input=user_prompt,
        conversation=conversation.id,
        model=os.environ["FOUNDRY_MODEL"],
        extra_body={"agent_reference": {"name": "agent1", "type": "agent_reference"}},
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                response_text += event.delta
                yield response_text


gr.ChatInterface(fn=stream_chat).launch()
