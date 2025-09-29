import boto3
import json

def test_claude_2():
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    body = json.dumps({
        "prompt": "\n\nHuman: Can you explain a solar eclipse in one sentence?\n\nAssistant:",
        "max_tokens_to_sample": 100,
        "temperature": 0.1
    })
    
    try:
        response = client.invoke_model(
            body=body,
            modelId='anthropic.claude-v2',
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        print("Success:", response_body['completion'])
        
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    test_claude_2()