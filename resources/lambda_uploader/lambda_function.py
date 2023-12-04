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
    try: 
        object_name=event['queryStringParameters']['upload']
    except:
        print("File name not exist")
    else:
        print(object_name)
        bucket_name="s3-organize-file"
        response=create_presigned_post(bucket_name, object_name, expiration=3600)
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
        
    try: 
        search_query=event['queryStringParameters']['query']
    except:
        print("File name not exist")
    else:
        table_name  = 'FilesMetadata'
        table = dynamodb.Table(table_name)
        response = table.scan(
            FilterExpression= 'contains(FileName :query)',
            ExpressionAttributeValues= {':query': {'S': search_query}}
        )
        
        #extract files name from dynamodb response
        file_names = [item['FileName']['S']for item in response['Items']]
        
        return {
            'statusCode': 200,
            'body': json.dumps(file_names)
        }
        
    try: 
        object_metadata = event['queryStringParameters']['metadata']
        metadata = json.loads(object_metadata)
        file_name = metadata['name']
        file_type = metadata['type']
        bucket_name = "s3-organize-file"
        region = "ap-northeast-1"
    except KeyError:
        print("File metadata not found in the query parameters")
    else:
        destination_folder  = metadata['type'] + "/"
            
        s3_client.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': file_name},
            Key=destination_folder + file_name
        )
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)

        response = upload_metadata(bucket_name, destination_folder, file_name, file_type, region)
        
        print(object_metadata)
        return {
            'statusCode': 200
        }

    
    
    
    