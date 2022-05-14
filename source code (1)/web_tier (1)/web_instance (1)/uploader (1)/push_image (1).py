import boto3
import io
import base64
import time
import subprocess
from properties import aws_properties as AWS

AWS_SERVER_ACCESS_KEY = AWS.AWS_SERVER_ACCESS_KEY
AWS_SERVER_SECRET_KEY = AWS.AWS_SERVER_SECRET_KEY
REGION_NAME = AWS.REGION_NAME
INPUT_BUCKET_NAME = AWS.INPUT_BUCKET_NAME
SQS_INPUT_NAME  = AWS.SQS_INPUT_NAME
SQS_INPUT_URL = AWS.SQS_INPUT_URL

sqs = boto3.resource('sqs', region_name=REGION_NAME,aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY)

def push_to_sqs(image_file):

    try:
        image = io.BufferedReader(image_file).read()
        image_filename = image_file.filename
        queue = sqs.get_queue_by_name(QueueName= SQS_INPUT_NAME)
        encoded_bytes = base64.b64encode(image)
        encoded_string=encoded_bytes.decode('utf-8')
        #result = queue.send_message(QueueUrl=SQS_INPUT_URL,MessageBody=encoded_string,MessageAttributes={ 'images': {'StringValue':image_filename,'DataType': 'String'}})
        queue.send_message(QueueUrl=SQS_INPUT_URL,MessageBody=encoded_string,MessageAttributes={ 'images': {'StringValue':image_filename,'DataType': 'String'}})
      
    except Exception as e:
        print(e)

def push_sqs_from_generator(image_file):

    try:
        image = image_file.read()
        image_filename = image_file.filename
        queue = sqs.get_queue_by_name(QueueName= SQS_INPUT_NAME)
        encoded_bytes = base64.b64encode(image)
        encoded_string=encoded_bytes.decode('utf-8')
        queue.send_message(QueueUrl=SQS_INPUT_URL,MessageBody=encoded_string,MessageAttributes={ 'images': {'StringValue':image_filename,'DataType': 'String'}})
        
    except Exception as e:
        print(e)