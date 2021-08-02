import json
from models import Invoice


def lambda_handler(event, context):
    if event.get('requestContext').get('http').get('method') == 'POST':
        body = json.loads(event.get('body'))
        invoice = Invoice(
            body['invoice_lines'],
            body['payments']
        )
        invoice.payments_categorisations()
        output = [
            {'id': payment.id,
             'categorisation': [
                 {
                     'category': item['category'],
                     'net_amount': str(item['net_amount'])
                 } for item in payment.categorisations]}
            for payment in invoice.payments]
    else:
        output = 'Post requests are expected'

    return {
        'statusCode': 200,
        'headers': {"content-type": "application/json"},
        'body': json.dumps(output)
    }
