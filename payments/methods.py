
from main.models import Templates, Accounts, AccountLogs, VPS, Usage
from django.contrib import messages
import datetime
from decimal import Decimal
from utils.ec2 import *
from utils.ec2 import get_client


import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging
from django.conf import settings
from django.http import JsonResponse


from django.contrib import messages
from django.db.models import Q

region = 'ap-south-1'
def get_client(obj):
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

    session = boto3.Session(
        aws_access_key_id=obj.aws_account.access,
        aws_secret_access_key=obj.aws_account.secret,
        region_name=region
    )
    return session.client('ec2')





def generate_instance(request, pk, order):
    template = Templates.objects.get(id=pk)
    cli_ = get_client(template)
    number_of_instances = 1
    try:
        response = create_instance(cli_, template.template_id, 1, 1)
        vpses = []
        try:
            for instance in response['Instances']:
                waiter = cli_.get_waiter('instance_running')
                res = waiter.wait(InstanceIds=[instance['InstanceId']])
                vps = VPS(
                    instance_id= instance['InstanceId'],
                    aws_account=template.aws_account,
                    obj_type = template.obj_type,
                    state= instance['State']['Name'],
                    created_by=order.customer,
                    template=template,
                    date_created=datetime.datetime.now()
                )
                vps.save()
                hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()
                vps.hostname = hostname
                vps.port = template.port
                vps.instance_user = template.user
                vps.instance_password = template.password
                vps.summary = summary
                vps.save()
                vpses.append(vps)
            return vpses[0]

        except Exception as e:
            messages.error(request, f'{e}')
            return None
    except Exception as e:
        messages.error(request, f'{e}')
        return None


