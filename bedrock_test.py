import boto3
import json

def invoke_claude(prompt):
    client = boto3.client(service_name="bedrock-runtime")

    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",  # ✅ valid modelId
        body=json.dumps({
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        }),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["output_text"]  # ✅ Bedrock returns output_text for Claude

if __name__ == "__main__":
    answer = invoke_claude("Can you explain a solar eclipse?")
    print(answer)
