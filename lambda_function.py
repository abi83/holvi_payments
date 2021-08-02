import json
from models import Invoice


def lambda_handler(event, context):
    if event.get('requestContext').get('http').get('method') == 'POST':
        body = json.loads(event.get('body'))
        print('Parsed body:', body)
        # invoice_lines = body['invoice_lines']
        invoice = Invoice(
            body['invoice_lines'],
            body['payments']
        )
        print('Invoice', invoice)
    else:
        body = 'Post requests are expected'
        print('GET')

    return {
        'statusCode': 200,
        'headers': {"content-type": "application/json"},
        'body': json.dumps(body)
    }
