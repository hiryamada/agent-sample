from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
import os


project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=AzureCliCredential()
)
openai = project.get_openai_client()
response = openai.responses.create(
    input="こんにちは",
    model=os.environ["FOUNDRY_MODEL"],
    extra_body={"agent_reference": {"name": "agent1", "type": "agent_reference"}},
)
print(response.output_text)
