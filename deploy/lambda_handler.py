#!/usr/bin/env python3
import json
from src.agent import run_agent

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        prompt = body.get('prompt', '')
        result = run_agent(prompt)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
