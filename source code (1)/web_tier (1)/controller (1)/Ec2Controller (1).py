import boto3
from properties import aws_properties as AWS
from botocore.exceptions import ClientError
import time

AWS_SERVER_ACCESS_KEY = AWS.AWS_SERVER_ACCESS_KEY
AWS_SERVER_SECRET_KEY = AWS.AWS_SERVER_SECRET_KEY
REGION_NAME = AWS.REGION_NAME
SQS_INPUT_URL = AWS.SQS_INPUT_URL
IMAGE_ID = AWS.IMAGE_ID
#USER_DATA = AWS.USER_DATA
KEYPAIR = AWS.KEYPAIR

sqs_client = boto3.client('sqs', aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY, region_name=REGION_NAME)
ec2_client = boto3.client('ec2', aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY, region_name=REGION_NAME)
ec2_resource = boto3.resource('ec2', aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY,region_name=REGION_NAME)                        

def run_instance(image_id, maxinstances, count):

    min_instances = maxinstances - 1
    max_instances = maxinstances
    
    if (min_instances == 0):
        min_instances = 1
        
    security_group = ['launch-wizard-3']
    
    TAG_SPEC = [{
    "ResourceType":"instance",
    "Tags": [
            {
                "Key": "Name",
                "Value": "worker_app-instance"+str(count)
            }
            ]
                }]
    
    instances = ec2_client.run_instances(ImageId=image_id, MinCount= min_instances, MaxCount= max_instances, InstanceType="t2.micro", KeyName=KEYPAIR , SecurityGroups=security_group, TagSpecifications = TAG_SPEC)
    

def getTotalMessagesCount():

    response = sqs_client.get_queue_attributes(QueueUrl=SQS_INPUT_URL,AttributeNames=['ApproximateNumberOfMessages'])
    return int(response['Attributes']['ApproximateNumberOfMessages'])

def getRunningInstances():

    running_instances = ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','pending']}])
    cnt=0
    for instance in running_instances:
        cnt=cnt+1
        print (instance.id, instance.instance_type)
    return cnt

def ScaleInScaleOut():
    cnt=0
    while(True):
        total_no_of_messages = getTotalMessagesCount()
        running_instances = getRunningInstances()
        total_app_instances = running_instances - 1
        print("Messages in the input queue are :{}".format(total_no_of_messages))
        print("Total Application Instances are:{} ".format(total_app_instances)) 

        if(total_no_of_messages > 0 and total_no_of_messages > total_app_instances): 
            t = 19 - total_app_instances
            if t>0:
                t1 = total_no_of_messages - total_app_instances							
                minInstances = min(t, t1)
                for i in range(minInstances): 
                    run_instance(IMAGE_ID, 1, i+1)
                cnt+=1 
        try:
            time.sleep(3)
        except Exception as e:
            print(e)

if __name__=='__main__':
        
    ScaleInScaleOut()   