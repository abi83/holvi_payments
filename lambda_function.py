import json

import base64


def lambda_handler(event, context):
    if event.get('requestContext').get('http').get('method') == 'POST':
        base64_body = event.get('body')
        base64_bytes = base64_body.encode('ascii')
        body_bytes = base64.b64decode(base64_bytes)
        body = json.loads(body_bytes.decode('ascii'))
        print('Parsed body:', body)
    else:
        print('GET')

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
