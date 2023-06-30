# current_date = ''
# instance_id = ''
# dynamo_table_name = 'DNSAutonamer' #THIS TABLE EXISTS IN FASTUP DEV ACCOUNT. THIS SHOULD BE REPLACED WITH CLIENT TABLE.
# hosted_zone_record_id = 'Z3H9N4EGU09IN2' #THIS IS FOR FASTUP DEV ACCOUNT.
# domain_name = '.dev.fastup.com' #THIS IS FOR FASTUP DEV ACCOUNT. FOR CLIENT IT WILL BE '.4tk.me'.
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import datetime
from botocore.exceptions import ClientError
from decimal import Decimal


current_date = ''
instance_id = ''
dynamo_table_name = 'DnsAutoNamerTable' 
hosted_zone_record_id = 'Z055259535QD5UWDVUUE1' 
domain_name = '.4ttk.de' 

master_acc_id = "570117161101"
role_name = "DnsAutoNamerRole"
ec2_client = boto3.client('ec2')


def lambda_handler(event, context):
    print(event)
    cross_acc_id = event["account"]
    print(cross_acc_id)
    client_region = event["region"]
    print(client_region)
    if event['source'] == 'aws.ec2' and event['detail-type'] == 'EC2 Instance State-change Notification' and \
            event['detail']['state'] == 'running':
        print("Starting to handle new running instance")
        instance_id = event['detail']['instance-id']
        print("New instance id : " + instance_id)
        if cross_acc_id != master_acc_id:
            print("line42")
            assume_role_arn = "arn:aws:iam::" + cross_acc_id + ":role/" + role_name
            get_cross_acc_client(assume_role_arn, client_region)
            response = cross_ec2.describe_instances(InstanceIds=[instance_id], )
            print(response)
        else:
            print("line48")
            response = ec2_client.describe_instances(InstanceIds=[instance_id], )
        print("Done describing new instance")
        print(response)
        if 'PublicIpAddress' in response['Reservations'][0]['Instances'][0]:
            ip_addr = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            print("Found public ip for new instance")
            print(ip_addr)
        else:
            ip_addr = response['Reservations'][0]['Instances'][0]['PrivateIpAddress']
            print("Did not find public ip, using PRIVATE IP address")
            print(ip_addr)

        query_dynamo(instance_id, ip_addr, cross_acc_id, event)
    else:
        print("This is not a new instance launching or an existing instance starting")

def get_cross_acc_client(role_arn, region):
    sts_client = boto3.client('sts')
    credientials = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='EC2-AutoNamer-Session'
    )
    access_key = credientials['Credentials']['AccessKeyId']
    secret_key = credientials['Credentials']['SecretAccessKey']
    session_key = credientials['Credentials']['SessionToken']
    global cross_ec2
    cross_ec2 = boto3.client('ec2',
                             region_name=region,
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key,
                             aws_session_token=session_key
                             )


def query_dynamo(instance_id, ip_addr, cross_acc_id, event):
    dynamo_client = boto3.resource('dynamodb')
    table_name = dynamo_client.Table(dynamo_table_name)
    response = table_name.query(
        KeyConditionExpression=Key('keyname').eq(instance_id +"+"+ cross_acc_id)
    )
    print(response)
    if response['Count'] == 1:
        print("Found one instance in dynamodb of provided instance id "+ instance_id)
        print("Will proceed with remapping dns to new IP "+ ip_addr)
        hosted_record_name = response['Items'][0]['hostname']
        print(ip_addr + " will be mapped to existing name " + hosted_record_name)
        hosted_zone_id = hosted_zone_record_id
        update_dns(hosted_record_name, hosted_zone_id, ip_addr)
    else:
        print("Did not find an existing instance, proceeding with creating new name for new instance with id " + instance_id + " and ip " + ip_addr)
        response = table_name.query(
            KeyConditionExpression=Key('keyname').eq('serial_number')
        )
        print ("found the serial number item in db")
        print(response)
        db_date = response['Items'][0]['datestring']
        serial_number = response['Items'][0]['serial_number']
        original_s_n = serial_number
        

        db_date_dt = datetime.datetime.strptime(db_date, "%d%m%y")
        current_date = datetime.datetime.now().strftime("%d%m%y")
        dd_mm = datetime.datetime.now().strftime("%d%m")
        current_dt = datetime.datetime.strptime(current_date, "%d%m%y")
        print("current_date")
        print(current_date)
        print("db_date")
        print(db_date)
        if current_dt > db_date_dt:
            print("current date is past the date in the db. Proceeding to update date")
            serial_update = table_name.update_item(
                Key={
                    'keyname': 'serial_number'
                },
                UpdateExpression="set serial_number=:serial_number, datestring=:datestring",
                ExpressionAttributeValues={
                    ":serial_number": 11111,
                    ":datestring": current_date
                })
            print("updated db serial number to 11111 and date to "+ current_date)
            print(serial_update)
            lambda_handler(event, None)
        elif current_dt == db_date_dt:
            print("current date is same as date in database. Proceeding to create new name")
            serial_number += 1
            try:
                serial_update = table_name.update_item(
                    Key={
                        'keyname': 'serial_number'
                    },
                    ConditionExpression=Attr('serial_number').eq(original_s_n),
                    UpdateExpression="set serial_number=:serial_number",
                    ExpressionAttributeValues={
                        ":serial_number": serial_number
                    })
                print("updated serial number to " + str(serial_number))
            except ClientError as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    print(e.response['Error'])
                    print("something else already updated serial number, will try again.")
                    lambda_handler(event, None)
            hosted_record_name = 'awsproxy' + dd_mm + get_serial() + str(serial_number) + domain_name
            increment_serial()
            hosted_zone_id = hosted_zone_record_id
            add_dns_record(instance_id, hosted_record_name, cross_acc_id)
            update_dns(hosted_record_name, hosted_zone_id, ip_addr)
        else:
            print("current_dt is less than db_date")


def update_dns(record_name, zone_id, ip_addr):
    route53_client = boto3.client('route53')
    response = route53_client.change_resource_record_sets(
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'ResourceRecords': [
                            {
                                'Value': ip_addr,
                            },
                        ],
                        'TTL': 300,
                        'Type': 'A',
                    },
                },
            ],
            'Comment': 'ec2-record',
        },
        HostedZoneId=zone_id,
    )
    print("Done updating dns to " + record_name + " for ip " + ip_addr)


def add_dns_record(instance_id, record_name, cross_acc_id):
    print('instance_id:', str(instance_id))
    dynamo_client = boto3.client('dynamodb')
    put_response = dynamo_client.put_item(
        Item={
            'keyname': {'S': str(instance_id)+"+"+str(cross_acc_id)},
            'hostname': {'S': record_name}
        },
        TableName=dynamo_table_name
    )


def get_serial():
    dynamo_client = boto3.resource('dynamodb',"ap-south-1")
    table_name = dynamo_client.Table("countSettingTable")
    response = table_name.get_item(
        Key={
            'id': 1,
        }
    )
    return response['Item']['instances']



def increment_serial():
    dynamo_client = boto3.resource('dynamodb',"ap-south-1")
    table_name = dynamo_client.Table("countSettingTable")
    response = table_name.update_item(
        Key={
            'id': 1
        },
        UpdateExpression="SET instances = if_not_exists(instances, :start) + :inc",
        ExpressionAttributeValues={
            ':inc': 1,
            ':start': 0,
        },
    )
    return 