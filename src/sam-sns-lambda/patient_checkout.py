import json
def handler(event, context):
  patients = [{'name': json.loads(record['Sns']['Message'])['name'], 'status': 'checkout'} for record in event['Records']]
  print(patients)
