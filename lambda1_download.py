import boto3
import requests

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    url = "https://www.sec.gov/files/company_tickers.json"  # replace with the actual URL
    response = requests.get(url)
    s3.put_object(Bucket='your-bucket-name', Key='company_tickers.json', Body=response.content)
