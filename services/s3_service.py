import boto3

s3 = boto3.client(
    "s3",
    region_name="us-east-1",
    verify=False
)

def upload_file(bucket_name, object_name, data):

    s3.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=data
    )

def download_file(bucket_name, object_name):

    response = s3.get_object(
        Bucket=bucket_name,
        Key=object_name
    )

    return response["Body"].read()

def list_files(bucket_name):

    response = s3.list_objects_v2(
        Bucket=bucket_name
    )

    return response.get("Contents", [])

def download_file(bucket_name, object_name):

    response = s3.get_object(
        Bucket=bucket_name,
        Key=object_name
    )

    return response["Body"].read()