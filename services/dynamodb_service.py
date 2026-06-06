import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    verify=False
)

def save_document_metadata(
        table_name,
        employee_id,
        file_name,
        document_type):

    table = dynamodb.Table(table_name)

    table.put_item(
        Item={
            "employee_id": employee_id,
            "file_name": file_name,
            "document_type": document_type,
            "upload_time": datetime.utcnow().isoformat()
        }
    )

def get_documents(table_name, employee_id):

    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=
        Key("employee_id").eq(employee_id)
    )

    return response["Items"]

def get_all_documents(table_name):

    table = dynamodb.Table(table_name)

    response = table.scan()

    return response["Items"]