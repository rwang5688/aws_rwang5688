import os
import json
        
def lambda_handler(event, context):
    region = os.environ['AWS_REGION']
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Greeting": "Hello World from lambda_handler!",
            "Region": region,
            "Version": "0.1"
        })
    }

    return response

