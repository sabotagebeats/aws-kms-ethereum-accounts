import boto3
import json

lambda_client = boto3.client('lambda')

test_event = {
    "operation": "sign",
    "amount": 1,
    "dst_address": "",
    "nonce": 1,
    "data": "0x000",
    "gas": 160000,
    "gasPrice": "0x0918400000"
}

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