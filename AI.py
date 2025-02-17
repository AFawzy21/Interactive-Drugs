# pip install azure-ai-inference
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


api_key = os.getenv("AZURE_INFERENCE_CREDENTIAL", '')
if not api_key:
  raise Exception("A key should be provided to invoke the endpoint")

client = ChatCompletionsClient(
    endpoint='https://DeepSeek-R1-refno.eastus2.models.ai.azure.com',
    credential=AzureKeyCredential(api_key)
)

model_info = client.get_model_info()
# print("Model name:", model_info.model_name)
# print("Model type:", model_info.model_type)
# print("Model provider name:", model_info.model_provider_name)



@app.route('/combine', methods=['POST'])
def Drugs_combination():
    data = request.get_json()

    joined_Data=", ".join(data["drugs"])
    payload = {
  "messages": [
    {
      "role": "user",
      "content": """Determine the drug-drug interaction class between """+joined_Data+""" including the reason for any interaction, and list food interactions for each drug. I'm expecting the output in the following json format { "DrugDrugInteraction": "High", "DrugDrugInteractionReason": "Bla Bla Bla", "FoodInteractions": { "Drug1": ["inter 1", "inter 2", "inter 3"], "Drug2": ["inter 4", "inter 5", "inter 6"], "Drug2": [] } }"""
    }
  ],
  "max_tokens": 10000
    }
    response = client.complete(payload, timeout=300)

    response_content = response.choices[0].message.content

    # Find the JSON part of the response
    start_index = response_content.find("{")
    end_index = response_content.rfind("}") + 1
    json_str = response_content[start_index:end_index]

    # Parse the JSON string
    data = json.loads(json_str)

    # Print the extracted JSON data

    print("Response:", response.choices[0].message.content)
    print(json.dumps(data, indent=2))
    print("Model:", response.model)
    print("Usage:")
    print("	Prompt tokens:", response.usage.prompt_tokens)
    print("	Total tokens:", response.usage.total_tokens)
    print("	Completion tokens:", response.usage.completion_tokens)
    return json.dumps(data, indent=2)

if __name__ == '__main__':
    app.run(debug=True)