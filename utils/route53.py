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
hosted_zone_record_id = 'Z06508551E3UE5N5C7FXS' 
domain_name = '.4tp.link'
access = ''
secret = ''

def update_route53(obj, summary):
    session = boto3.Session(
        aws_access_key_id=obj.aws_account.access,
        aws_secret_access_key=obj.aws_account.secret,
        region_name=region
    )
    route53_client = session.client('route53')
    response = ''
    try:
        response = route53_client.change_resource_record_sets(
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': summary,
                            'ResourceRecords': [
                                {
                                    'Value': "ip_not_set",
                                },
                            ],
                            'TTL': 300,
                            'Type': 'A',
                        },
                    },
                ],
                'Comment': summary,
            },
            HostedZoneId=hosted_zone_record_id,
        )
        print("Done updating dns to " + summary + "  ")
        return True
    except Exception as e:
        print(e)
        print(response)
        return False
    