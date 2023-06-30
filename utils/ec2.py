import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging
from django.conf import settings
from django.http import JsonResponse

# session = boto3.Session(
#     aws_access_key_id=settings.ACCESS_ID,
#     aws_secret_access_key=settings.ACCESS_KEY,
# )
# ec2_client = session.resource('ec2')

# ec2_client = boto3.client('ec2', 
#                     aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY, 
#                     aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY, 
#                     region_name='us-east-1'
#                     )


from django.contrib import messages
from django.db.models import Q

region = 'ap-south-1'
def get_client(obj, user, VPS):
    if obj.obj_type == 'vps':
        session = boto3.Session(
            aws_access_key_id=obj.aws_account.access,
            aws_secret_access_key=obj.aws_account.secret,
            region_name=region
        )
        return session.client('ec2')


    elif obj.obj_type == 'proxy':
        session = boto3.Session(
            aws_access_key_id=obj.aws_account.access,
            aws_secret_access_key=obj.aws_account.secret,
            region_name=region
        )
        return session.client('ec2')

    return None


def client(obj):
    session = boto3.Session(
        aws_access_key_id=obj.aws_account.access,
        aws_secret_access_key=obj.aws_account.secret,
        region_name=region
    )
    return session.client('ec2')


def get_all_instances(client):
    try:
        response = ec2_client.describe_instances()
        return response
    except ClientError as e:
        logging.error(e)
        raise e
    
def instance_description(client, instanceId):
    try:
        response = client.describe_instances(
            InstanceIds=[
                instanceId,
            ],
        )
        return response['Reservations']['Instances'][0]
    except ClientError as e:
        logging.error(e)
        raise e

def create_instance(client, TemplateId,MinCount, MaxCount):

    try:
        instances = client.run_instances(
            LaunchTemplate={'LaunchTemplateId': TemplateId},
            MinCount=1,
            MaxCount=1,
        )
        return instances
    except ClientError as e:
        print(e)
        return e







def create_instance_from_template(client, ImageId,MinCount, MaxCount, InstanceType, KeyName):
    instances = ec2_client.run_instances(
        ImageId=ImageId,
        MinCount=MinCount,
        MaxCount=MaxCount,
        InstanceType=InstanceType,
        KeyName=KeyName
    )
    return instances

def test(request):
    response = instance_description('i-0b0d150ea26f1b712')
    return JsonResponse(response)

def reboot_instance(client, InstanceId):
    try:
        response = ec2.reboot_instances(InstanceIds=['INSTANCE_ID'], DryRun=False)
        print('Success', response)
    except ClientError as e:
        print('Error', e)




def terminate_instance(client, InstanceId):
    try:
        response = ec2.terminate_instances(InstanceIds=['INSTANCE_ID'], DryRun=False)
        print('Success', response)
    except ClientError as e:
        print('Error', e)
# import boto3
# client = boto3.client('ec2')
# data = client.get_launch_template_data(InstanceId='i-0d648aXXXXXX9af2')