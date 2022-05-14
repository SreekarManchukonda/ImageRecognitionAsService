import boto3
import os
import subprocess
import terminate
from properties import aws_properties as AWS

AWS_SERVER_ACCESS_KEY = AWS.AWS_SERVER_ACCESS_KEY
AWS_SERVER_SECRET_KEY = AWS.AWS_SERVER_SECRET_KEY
REGION_NAME = AWS.REGION_NAME
OUTPUT_BUCKET_NAME = AWS.OUTPUT_BUCKET_NAME
SQS_OUTPUT_NAME  = AWS.SQS_OUTPUT_NAME
SQS_OUTPUT_URL = AWS.SQS_OUTPUT_URL
SQS_INPUT_URL = AWS.SQS_INPUT_URL

sqs = boto3.resource('sqs', region_name=REGION_NAME,aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY)
queue = sqs.get_queue_by_name(QueueName= SQS_OUTPUT_NAME)
sqs_client = boto3.client('sqs',region_name=REGION_NAME,aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY)
s3 = boto3.client('s3', aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key = AWS_SERVER_SECRET_KEY, region_name=REGION_NAME)

def get_sqs_messages_count():
    try:
        response = sqs_client.get_queue_attributes(QueueUrl=SQS_INPUT_URL,AttributeNames=['ApproximateNumberOfMessages'])
        return int(response['Attributes']['ApproximateNumberOfMessages'])
    except Exception as e:
        print(e)

def upload_to_s3(keyname,data):
    
    try:
        
        res_s3 = s3.put_object(Body=data, Bucket=OUTPUT_BUCKET_NAME, Key=keyname)
        
        
        return res_s3['ResponseMetadata']['HTTPStatusCode']

    except Exception as e:
        print(e)

def send_message():
    
    path = os.path.dirname(os.getcwd())
    path1 = os.path.join(path, 'image_recognition')
    path2 = os.path.join(path1, 'result.txt')
    f = open(path2, "r")
    text = f.read()
    filename = text.split('#')[0]
    value = text.split('#')[1]
    keyname = filename.split('.')[0]
    data = '('+keyname+','+value+')'
    
    response = upload_to_s3(keyname,data)
    if(response==200):
        try:
            queue.send_message(QueueUrl=SQS_OUTPUT_URL,MessageBody=value,MessageAttributes={ 'output': {'StringValue':filename,'DataType': 'String'}})
            count = get_sqs_messages_count()
            print(count)
            if(count):
                subprocess.call(['sh', '/home/ec2-user/app_tier/app_tier.sh'])
            else:
                
                terminate.terminate()

        except Exception as e:
            print(e)

    print("Send Message completed")
    
    

    
if __name__ == '__main__':

    send_message()