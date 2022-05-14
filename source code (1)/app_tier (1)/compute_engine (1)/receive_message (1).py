import boto3
import base64
from PIL import Image
import terminate
import io
import os
from properties import aws_properties as AWS

AWS_SERVER_ACCESS_KEY = AWS.AWS_SERVER_ACCESS_KEY
AWS_SERVER_SECRET_KEY = AWS.AWS_SERVER_SECRET_KEY
REGION_NAME = AWS.REGION_NAME
INPUT_BUCKET_NAME = AWS.INPUT_BUCKET_NAME
SQS_INPUT_NAME  = AWS.SQS_INPUT_NAME
SQS_INPUT_URL = AWS.SQS_INPUT_URL

sqs = boto3.resource('sqs', region_name=REGION_NAME,aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY)
sqs_client = boto3.client('sqs',aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key = AWS_SERVER_SECRET_KEY, region_name=REGION_NAME)

s3 = boto3.client('s3', aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key = AWS_SERVER_SECRET_KEY, region_name=REGION_NAME)


def receive_message():
    
    try:
        print('Entered receive_message')
        queue = sqs.get_queue_by_name(QueueName= SQS_INPUT_NAME)
        result = queue.receive_messages(MessageAttributeNames=['images'],VisibilityTimeout=25,WaitTimeSeconds=1)
        if(result):
            filename = result[0].message_attributes.get('images').get('StringValue')
            image_bytes = result[0].body
            image_data = base64.b64decode(image_bytes)
            #byte_data = io.BytesIO(image_data)
            
            path = os.getcwd()
            path = os.path.dirname(path)
            
            path = os.path.join(path, 'image_recognition')
            upload_image = os.path.join(path, filename)
            
            f=open(upload_image,"wb")
            f.write(image_data)
            f.close()
            try:
                s3.upload_file(upload_image,Bucket=INPUT_BUCKET_NAME,Key=filename)
                
                sqs_client.delete_message(QueueUrl=SQS_INPUT_URL , ReceiptHandle=result[0].receipt_handle)
            except Exception as e:
                print(e)
        else:
            
            terminate.terminate()

    except Exception as e:
        print(e)
    
if __name__ == '__main__':
    
    receive_message()