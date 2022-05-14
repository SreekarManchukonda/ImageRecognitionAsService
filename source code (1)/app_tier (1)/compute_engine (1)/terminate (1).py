import boto3
from properties import aws_properties as AWS
from ec2_metadata import ec2_metadata

ec2_client = boto3.client('ec2',region_name=AWS.REGION_NAME,aws_access_key_id=AWS.AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS.AWS_SERVER_SECRET_KEY)
def terminate():

    instance_id = ec2_metadata.instance_id
    print(instance_id)
    print('terminating instance')
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
