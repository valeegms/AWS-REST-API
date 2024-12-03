import mimetypes
from os import getenv
from xml.dom.minidom import Attr
import boto3

def random_string(length: int):
    import string
    import random
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_client(type: str):
    return boto3.client(type,
            aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=getenv("AWS_SESSION_TOKEN"),
            region_name=getenv("AWS_REGION")
        )
    
def create_resource(type: str):
    return boto3.resource(type,
            aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=getenv("AWS_SESSION_TOKEN"),
            region_name=getenv("AWS_REGION")
        )

def upload_file_to_s3(file, filename):
    try:
        mime_type, _ = mimetypes.guess_type(filename)
        
        s3 = create_client('s3')
        s3.upload_file(
            file,
            getenv('BUCKET_NAME'),
            filename,
            ExtraArgs={
                # "ACL": "public-read",
                "ContentType": mime_type or 'multipart/form-data'
            }
        )
    except boto3.exceptions.S3UploadFailedError as e:
        raise Exception(f"Upload failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    
def publish_message_to_sns(message: str, topic_arn: str):
    sns = create_client('sns')
    sns.publish(
        TopicArn=topic_arn,
        Message=message
    )
    
def put_item_to_dynamodb(table_name: str, item: dict):
    dynamodb = create_client('dynamodb')
    dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    
def scan_table(table_name: str, filter_expression: Attr):
    dynamodb = create_resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression=filter_expression
    )
    return response['Items']

def update_item_in_dynamodb(table_name: str, key: dict, update_expression: str, expression_attribute_values: dict):
    dynamodb = create_resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )