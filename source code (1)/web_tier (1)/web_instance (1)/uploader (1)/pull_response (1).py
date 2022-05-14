import boto3
from properties import aws_properties as AWS

AWS_SERVER_ACCESS_KEY = AWS.AWS_SERVER_ACCESS_KEY
AWS_SERVER_SECRET_KEY = AWS.AWS_SERVER_SECRET_KEY
REGION_NAME = AWS.REGION_NAME
SQS_OUTPUT_NAME  = AWS.SQS_OUTPUT_NAME
SQS_OUTPUT_URL = AWS.SQS_OUTPUT_URL

sqs = boto3.resource('sqs', region_name=REGION_NAME,aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY)
sqs_client = boto3.client('sqs',region_name=REGION_NAME,aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY)

def pull_from_sqs(userdict):
    queue = sqs.get_queue_by_name(QueueName= SQS_OUTPUT_NAME)
    for i in range(len(userdict)):
    #for key in userdict:
        try:
            while(True):
                result = queue.receive_messages(MessageAttributeNames=['output'],VisibilityTimeout=6,WaitTimeSeconds=1)
    
                if(result):
              
                    filename = result[0].message_attributes.get('output').get('StringValue')
                    if(not userdict[filename] and filename):
                        print('filename'+result[0].message_attributes.get('output').get('StringValue'))
                        filename = result[0].message_attributes.get('output').get('StringValue')
                        userdict[filename] = result[0].body
                        sqs_client.delete_message(QueueUrl=SQS_OUTPUT_URL , ReceiptHandle=result[0].receipt_handle)
                        break
     

        except Exception as e:
            print(e)
            return None
    return userdict

def pull_image_for_generator(userobj,name):
    queue = sqs.get_queue_by_name(QueueName= SQS_OUTPUT_NAME)
   
    while(not userobj.userdict[name]):
        try:
            while(True):
                result = queue.receive_messages(MessageAttributeNames=['output'],VisibilityTimeout=4,WaitTimeSeconds=1)
                if(result):
                    filename = result[0].message_attributes.get('output').get('StringValue')
                    if(not userobj.userdict[filename] and filename):
                   
                        print('filename'+result[0].message_attributes.get('output').get('StringValue'))
                       
                        userobj.userdict[filename] = result[0].body
                        sqs_client.delete_message(QueueUrl=SQS_OUTPUT_URL , ReceiptHandle=result[0].receipt_handle)
                        break
                    elif(userobj.userdict[filename] and filename):
                        sqs_client.delete_message(QueueUrl=SQS_OUTPUT_URL , ReceiptHandle=result[0].receipt_handle)
                        break
                elif(not result and userobj.userdict[name]):
                    break
        except Exception as e:
            print(e)
            return None
    return userobj

