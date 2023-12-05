import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

# Initialize boto3 to use the S3 client.
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def create_presigned_post(bucket_name, object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
        
    return response

def create_presigned_get(bucket_name, object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name
            },
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None
        
    return response
    


def upload_metadata(bucket_name, destination_folder, file_name, file_type, region):
    file_name = file_name.replace(" ","+")
    file_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{destination_folder}{file_name}"
    db_table = dynamodb.Table('FilesMetadata')
    
    response = db_table.put_item(
        Item={
            "FileName": file_name,
            "FileType": file_type,
            "FileUrl": file_url
        }
    )
    return response

def lambda_handler(event, context):
    httpMethod = event['httpMethod']
    path = event['path']
    
    if httpMethod == "POST" and path == "/url":
        try: 
            object_name = event['queryStringParameters']['upload']
            bucket_name = "s3-organize-file"
            response = create_presigned_post(bucket_name, object_name, expiration=3600)
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    if httpMethod == "POST" and path == "/files":
        try: 
            object_metadata = event['queryStringParameters']['metadata']
            metadata = json.loads(object_metadata)
            file_name = metadata['name']
            file_type = metadata['type']
            bucket_name = "s3-organize-file"
            region = "ap-northeast-1"

            destination_folder = metadata['type'] + "/"
                
            s3_client.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': file_name},
                Key=destination_folder + file_name
            )
            s3_client.delete_object(Bucket=bucket_name, Key=file_name)

            response = upload_metadata(bucket_name, destination_folder, file_name, file_type, region)

            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    if httpMethod == "GET" and path == "/files":
        try: 
            table_name = "FilesMetadata"
            table = dynamodb.Table(table_name)
            items = table.scan(AttributesToGet=['FileName', 'FileType'])
            return {
                'statusCode': 200,
                'body': json.dumps(items)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    if httpMethod == "GET" and path == "/url":
        try: 
            object_name = event['queryStringParameters']['download']
            bucket_name = "s3-organize-file"
            response = create_presigned_get(bucket_name, object_name, expiration=3600)
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    
    