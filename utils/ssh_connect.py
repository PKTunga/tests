import json
import logging
import boto3
import paramiko
dynamo_table_name = 'DnsAutoNamerTable' 

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging
from django.conf import settings
from django.http import JsonResponse


# from django.co
# from ec2 import client
import datetime

date_time = datetime.datetime.now()
from django.conf import settings
import os
def generate_key(client, obj, user):
  date = datetime.datetime.now()

  keypair_name = f'{obj.id}{user.id}{date.year}{date.month}{date.day}{date.hour}{date.minute}{date.second}.pem'
  try:
    try:
      response = client.create_key_pair(KeyName=keypair_name)
      print(response)
      try:
        private_key_file=open(os.path.join(settings.RDP_FOLDER, keypair_name),"w")
        private_key_file.write(response['KeyMaterial'])
        private_key_file.close
        return keypair_name
      except ClientError as e:
          print(e)
          return False
    except ValueError as e:
      return False
  except ValueError as e:
    return False


def update_password_port_user(client, obj, instance):
    print('GETTTING FILE')
    path = os.path.join(settings.RDP_FOLDER, obj.key_name)
    print(path)
    k = paramiko.RSAKey.from_private_key_file(path)
    print("Connecting")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    response = client.describe_instances(InstanceIds=[instance['InstanceId']])
    print(response)
    print('LLLLLLLLLLLLLLLLLLLLLLLLLLLL')
    print(response['Reservations']['instances'][0]['PrivateIpAddresses'][0])
    host=instance
    print("Connecting to " + host)
    c.connect( hostname = host, username = "centos", pkey = k )
    loggin.error(c)
    logging.error("Connected")
    print("Connected to " + host)
    port = ''
    password = ''
    summary = ''
    username = 'superuser'
    ID = ''
    sproxy_cfg = f"echo 'nscache 65536\ndaemon\nusers {username}:CL:Ticket1234\nauth strong\nallow *\nproxy -p{port} -a\nsetgid 99\nsetuid 99' > /etc/3proxy.cfg"
    commands = [
        "ls",
        "pwd",
        sproxy_cfg,
        'sudo systemctl restart 3proxy'
        ]
        
    for command in commands:
      stdin , stdout, stderr = c.exec_command(command)
      print(stdin)
      logging.error(stdin)

      print(stdout)
      logging.error(stdout)
      
      print(stderr)
      logging.error(stderr)
      
    res = update_table(client, port, ID, password, instance_id, cross_acc_id)
    return
      
      

def update_table(port, ID, password, instance_id,cross_acc_id ):
    dynamo_client = client.resource('dynamodb')
    table_name = dynamo_client.Table(dynamo_table_name)
    serial_update = table_name.update_item(
        Key={
            'keyname': instance_id + '+' + cross_acc_id
        },
        UpdateExpression="set port=:port, password=:password",
        ExpressionAttributeValues={
            ":port": port,
            ":password": password
        })
        
    return 




def password_already_changed(client, instance_id, cross_acc_id):
    dynamo_client = client.resource('dynamodb')
    table_name = dynamo_client.Table(dynamo_table_name)
    response = table_name.query(
        KeyConditionExpression=Key('keyname').eq(instance_id +"+"+ cross_acc_id)
    )
    print(response)
    if response['Count'] == 1:
      try:
          instance = response['Items'][0]
          try:
            updated = instance['updated']
            return updated
          except KeyError as e:
            raise False
      except IndexError as e:
        raise e
    else:
      return False
