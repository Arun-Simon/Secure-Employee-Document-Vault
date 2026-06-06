import boto3
import json

def get_secret():

    client = boto3.client(
        "secretsmanager",
        region_name="us-east-1",
        verify=False
    )

    response = client.get_secret_value(
        SecretId="secure-app-config"
    )

    return json.loads(
        response["SecretString"]
    )