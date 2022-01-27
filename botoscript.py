import boto3
import json

lambda_client = boto3.client('lambda')

input = open('input.json')

test_event = json.load(input)

input.close()

functions = lambda_client.list_functions()

name = functions['Functions'][0]['FunctionName']

response = lambda_client.invoke(
  FunctionName=name,
  Payload='{"operation":"status"}',
)

address = json.loads(response['Payload'].read().decode("utf-8"))['eth_checksum_address']

test_event['dst_address'] = address

response = lambda_client.invoke(
  FunctionName=name,
  Payload=json.dumps(test_event),
)

signed_tx = json.loads(response['Payload'].read().decode("utf-8"))['signed_tx']

r = signed_tx['r']
s = signed_tx['s']

print("r:",r)
print("s:",s)