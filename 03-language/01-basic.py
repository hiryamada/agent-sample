from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import AzureCliCredential
import os


endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
credential = AzureCliCredential()

text_analytics_client = TextAnalyticsClient(endpoint, credential)
result = text_analytics_client.detect_language(documents=["こんにちは"])
print(result[0])
