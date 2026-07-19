from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
import os


def main():
    project = AIProjectClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=AzureCliCredential()
    )
    openai = project.get_openai_client()
    conversation = openai.conversations.create()
    while True:
        prompt = input("ユーザー: ")
        if prompt == "exit":
            break

        with openai.responses.stream(
            input=prompt,
            conversation=conversation.id,
            model=os.environ["FOUNDRY_MODEL"],
            extra_body={
                "agent_reference": {"name": "agent1", "type": "agent_reference"}
            },
        ) as stream:
            print("エージェント: ", end="")
            for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="", flush=True)
            print()


if __name__ == "__main__":
    main()
