from pipes import Template
from django.shortcuts import get_object_or_404, render, redirect, reverse

from payments.models import OrderDetail
from .forms import VPSFORM, PROXYFORM, SuperUserVPSAccountForm,AdminAvailToSellerForm, SellerForm,AvailToSellerForm,AvailToSellerForm2, AvailToSellerForm3, AwsAccountsFORM, SuperUserPROXYAccountForm, TemplateFORM, ManualSuperUserPROXYAccountForm
from .models import VPS, Templates, SellerTemplates
from authenticate.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout, login as auth_login
from decimal import Decimal 
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError
from utils.ec2 import *
import pytz
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from utils.ec2 import get_client
from django.db.models import Q
from main.models import Accounts, AccountLogs
from packages.models import Packages
from authenticate.models import DailyNews,Video
from utils.ssh_connect import generate_key, update_password_port_user
from datetime import timezone
from .forms import ContactForm
import datetime 
from payments.models import OrderDetail
from authenticate.models import WhatsappNumber, BannerMessage

def index(request):
    user, new = WhatsappNumber.objects.get_or_create(id=1)
    banner, new = BannerMessage.objects.get_or_create(id=1)
    
    try:
        latest_video = Video.objects.latest("published_date")
        videoid = latest_video.video_id
    except Video.DoesNotExist:
        videoid = None
    
    context = {
        'form': ContactForm(),
        'packages': Packages.objects.all(),
        "dailyupdate": DailyNews.objects.latest("published_date").content,
        "videoid": videoid,
        'banner': banner,
        'whatapplink': f"https://wa.me/{user.number}"
    }
    
    return render(request, 'landing/i.html', context)

@login_required
def packages(request):
    context = {
        'packages': Packages.objects.all()
    }
    return render(request, 'landing/buy_now.html', context)


from packages.forms import ApplyCouponForm

@login_required
def buy(request, pk):
    context = {
        'package': Packages.objects.get(id=pk),
        'coupon_form': ApplyCouponForm()
    }
    return render(request, 'landing/buy.html', context)



from utils.ssh import update_instance_through_ssh
@login_required
def generate_seller_instance_superuser(request, pk):
    if request.method == "POST":
        print(request.POST)
        auto = request.POST.get('auto')
        number_of_instances = int(request.POST.get('no_of_instances'))
        s_template = SellerTemplates.objects.get(id=pk)
        template = s_template.template
        if template.generation == 'auto':
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            if account.balance >= (Decimal(s_template.cost) * Decimal(int(number_of_instances))):
                client = get_client(template, request.user, VPS)
                # key = generate_key(client, template, request.user)
                # print(key)
            
                if template.obj_type == 'vps':
                    # type_ = VPS.objects.filter(Q(obj_type='vps') &Q(user=request.user)).first()
                    response = create_instance(client, template.template_id, number_of_instances, number_of_instances)
                    print(response)
                    try:
                        for instance in response["Instances"]:
                            # instance = response['Instances'][0]
                            instance = instance
                            waiter = client.get_waiter('instance_running')
                            res = waiter.wait(InstanceIds=[instance['InstanceId']])
                            vps = VPS(
                                instance_id= instance['InstanceId'],
                                aws_account=template.aws_account,
                                obj_type = 'vps',
                                state= instance['State']['Name'],
                                created_by=request.user,
                                template=template,
                                date_created=datetime.datetime.now()

                                # key_name=key
                            )
                            vps.save()
                            # waiter = client.get_waiter('instance_running')
                            # res = waiter.wait(InstanceIds=[vps.instance_id])
                            hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()
                            # hostname = vps.update_hostname()
                            print(hostname)
                            # vps.date_generated = date
                            # vps.time_generated = time
                            vps.hostname = hostname
                            vps.port = template.port
                            vps.instance_user = template.user
                            vps.instance_password = template.password
                            vps.summary = summary
                            vps.save()
                            account.balance = Decimal(account.balance) - Decimal(s_template.cost)
                            account.save()
                            log = AccountLogs.objects.create(
                                description="Generated",
                                account=account,
                                amount=Decimal(s_template.cost) * -1,
                                balance=account.balance,
                                instance=vps,

                            )
                            log.save()
                            usage = Usage(
                                instance=vps,
                                start_date = datetime.datetime.now()
                            )
                            usage.save()
                            vps.current_usage = usage
                            vps.save()

                            print('Updating SSH')

                            # update_instance_through_ssh(client, template.aws_account, vps)

                    except Exception as e:
                        print(e)
                        messages.error(request, f'Something went wrong Please Contact The Administrator')
                elif template.obj_type == 'proxy':
                    # type_ = VPS.objects.filter(Q(obj_type='proxy') &Q(user=request.user)).first()
                    response = create_instance(client, template.template_id, number_of_instances, number_of_instances)
                    print(response)
                    try:
                        print("Connecting and trying")
                        for instance in response['Instances']:
                            # instance = response['Instances'][0]
                            print(instance)
                            waiter = client.get_waiter('instance_running')
                            res = waiter.wait(InstanceIds=[instance['InstanceId']])
                            vps = VPS(
                                instance_id= instance['InstanceId'],
                                aws_account=template.aws_account,
                                obj_type = 'proxy',
                                state= instance['State']['Name'],
                                created_by=request.user,
                                template=template,
                                date_created=datetime.datetime.now()

                                # key_name=key

                            )
                            vps.save()
                            print('Created Instance')
                            # waiter = client.get_waiter('instance_running')
                            # res = waiter.wait(InstanceIds=[vps.instance_id])
                            hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()

                            # hostname = vps.update_hostname()
                            print(hostname)
                            vps.hostname = hostname
                            vps.port = template.port
                            vps.instance_user = template.user
                            vps.instance_password = template.password
                            vps.summary = summary
                            vps.save()
                            account.balance = Decimal(account.balance) - Decimal(s_template.cost)
                            account.save()
                            log = AccountLogs.objects.create(
                                description="Generated",
                                account=account,
                                amount=Decimal(s_template.cost) * -1,
                                balance=account.balance,
                                instance=vps
                            )
                            log.save()
                            usage = Usage(
                                instance=vps,
                                start_date = datetime.datetime.now()
                            )
                            usage.save()
                            vps.current_usage = usage
                            vps.save()

                            messages.success(request, f'Successfully created')

                    except Exception as e:
                        print(e)

                        messages.error(request, f'Something went wrong Please Contact The Administrator')
            
            else:
                messages.error(request, f"Your Account does have enough balance to generate the {number_of_instances} instance")
        elif template.generation == 'manual':
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            if account.balance >= (Decimal(s_template.cost) * Decimal(int(number_of_instances))):
                objects = VPS.objects.filter(Q(template=template) & Q(assigned=False))
                if len(objects) == 0:
                    messages.success(request, f'Could Not Generate Proxy. Please contact the Administrator to generate more')
                elif len(objects) >= number_of_instances:
                    for i in range(number_of_instances):
                        vps = VPS.objects.get(id=objects[i].id)
                        vps.date_created = datetime.datetime.now()
                        vps.created_by = request.user
                        vps.assigned = True
                        vps.save()

                        account.balance = Decimal(account.balance) - Decimal(s_template.cost)
                        account.save()
                        log = AccountLogs.objects.create(
                            description="Generated",
                            account=account,
                            amount=Decimal(s_template.cost) * -1,
                            balance=account.balance,
                            instance=vps,

                        )
                        log.save()
                        usage = Usage(
                            instance=vps,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        vps.current_usage = usage
                        vps.save()

                elif len(objects) < number_of_instances:
                    for i in range(len(objects)):
                        vps = VPS.objects.get(id=i.id)
                        vps.date_created = datetime.datetime.now()
                        vps.created_by = request.user
                        vps.assigned = True
                        vps.save()

                        account.balance = Decimal(account.balance) - Decimal(s_template.cost)
                        account.save()
                        log = AccountLogs.objects.create(
                            description="Generated",
                            account=account,
                            amount=Decimal(s_template.cost) * -1,
                            balance=account.balance,
                            instance=vps,

                        )
                        log.save()
                        usage = Usage(
                            instance=vps,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        vps.current_usage = usage
                        vps.save()
                messages.success(request, f'Generated proxies. Please contact the Administrator to generate more')
            else:
                messages.success(request, f'Your account balance not enough')
    return redirect(reverse('superuser_home'))











from utils.ssh import update_instance_through_ssh
@login_required
def generate_instance(request, pk):

    if request.method == "POST":
        print(request.POST)
        auto = request.POST.get('auto')
        number_of_instances = int(request.POST.get('no_of_instances'))

        template = Templates.objects.get(id=pk)

        if template.generation == 'auto':
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            if account.balance >= (Decimal(template.cost) * Decimal(int(number_of_instances))):
                client = get_client(template, request.user, VPS)
                # key = generate_key(client, template, request.user)
                # print(key)
            
                if template.obj_type == 'vps':
                    # type_ = VPS.objects.filter(Q(obj_type='vps') &Q(user=request.user)).first()
                    response = create_instance(client, template.template_id, number_of_instances, number_of_instances)
                    print(response)
                    try:
                        for instance in response["Instances"]:
                            # instance = response['Instances'][0]
                            instance = instance
                            waiter = client.get_waiter('instance_running')
                            res = waiter.wait(InstanceIds=[instance['InstanceId']])
                            vps = VPS(
                                instance_id= instance['InstanceId'],
                                aws_account=template.aws_account,
                                obj_type = 'vps',
                                state= instance['State']['Name'],
                                created_by=request.user,
                                template=template,
                                date_created=datetime.datetime.now()

                                # key_name=key
                            )
                            vps.save()
                            # waiter = client.get_waiter('instance_running')
                            # res = waiter.wait(InstanceIds=[vps.instance_id])
                            hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()
                            # hostname = vps.update_hostname()
                            print(hostname)
                            # vps.date_generated = date
                            # vps.time_generated = time
                            vps.hostname = hostname
                            vps.port = template.port
                            vps.instance_user = template.user
                            vps.instance_password = template.password
                            vps.summary = summary
                            vps.save()
                            account.balance = Decimal(account.balance) - Decimal(template.cost)
                            account.save()
                            log = AccountLogs.objects.create(
                                description="Generated",
                                account=account,
                                amount=Decimal(template.cost) * -1,
                                balance=account.balance,
                                instance=vps,

                            )
                            log.save()
                            usage = Usage(
                                instance=vps,
                                start_date = datetime.datetime.now()
                            )
                            usage.save()
                            vps.current_usage = usage
                            vps.save()

                            print('Updating SSH')

                            # update_instance_through_ssh(client, template.aws_account, vps)

                    except Exception as e:
                        print(e)
                        messages.error(request, f'Something went wrong Please Contact The Administrator')
                elif template.obj_type == 'proxy':
                    # type_ = VPS.objects.filter(Q(obj_type='proxy') &Q(user=request.user)).first()
                    response = create_instance(client, template.template_id, number_of_instances, number_of_instances)
                    print(response)
                    try:
                        print("Connecting and trying")
                        for instance in response['Instances']:
                            # instance = response['Instances'][0]
                            print(instance)
                            waiter = client.get_waiter('instance_running')
                            res = waiter.wait(InstanceIds=[instance['InstanceId']])
                            vps = VPS(
                                instance_id= instance['InstanceId'],
                                aws_account=template.aws_account,
                                obj_type = 'proxy',
                                state= instance['State']['Name'],
                                created_by=request.user,
                                template=template,
                                date_created=datetime.datetime.now()

                                # key_name=key

                            )
                            vps.save()
                            print('Created Instance')
                            # waiter = client.get_waiter('instance_running')
                            # res = waiter.wait(InstanceIds=[vps.instance_id])
                            hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()

                            # hostname = vps.update_hostname()
                            print(hostname)
                            vps.hostname = hostname
                            vps.port = template.port
                            vps.instance_user = template.user
                            vps.instance_password = template.password
                            vps.summary = summary
                            vps.save()
                            account.balance = Decimal(account.balance) - Decimal(template.cost)
                            account.save()
                            log = AccountLogs.objects.create(
                                description="Generated",
                                account=account,
                                amount=Decimal(template.cost) * -1,
                                balance=account.balance,
                                instance=vps
                            )
                            log.save()
                            usage = Usage(
                                instance=vps,
                                start_date = datetime.datetime.now()
                            )
                            usage.save()
                            vps.current_usage = usage
                            vps.save()

                            messages.success(request, f'Successfully created')

                    except Exception as e:
                        print(e)

                        messages.error(request, f'Something went wrong Please Contact The Administrator')
            
            else:
                messages.error(request, f"Your Account does have enough balance to generate the {number_of_instances} instance")
        elif template.generation == 'manual':
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            if account.balance >= (Decimal(template.cost) * Decimal(int(number_of_instances))):
                objects = VPS.objects.filter(Q(template=template) & Q(assigned=False))
                if len(objects) == 0:
                    messages.success(request, f'Could Not Generate Proxy. Please contact the Administrator to generate more')
                elif len(objects) >= number_of_instances:
                    for i in range(number_of_instances):
                        vps = VPS.objects.get(id=objects[i].id)
                        vps.date_created = datetime.datetime.now()
                        vps.created_by = request.user
                        vps.assigned = True
                        vps.save()

                        account.balance = Decimal(account.balance) - Decimal(template.cost)
                        account.save()
                        log = AccountLogs.objects.create(
                            description="Generated",
                            account=account,
                            amount=Decimal(template.cost) * -1,
                            balance=account.balance,
                            instance=vps,

                        )
                        log.save()
                        usage = Usage(
                            instance=vps,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        vps.current_usage = usage
                        vps.save()

                elif len(objects) < number_of_instances:
                    for i in range(len(objects)):
                        vps = VPS.objects.get(id=i.id)
                        vps.date_created = datetime.datetime.now()
                        vps.created_by = request.user
                        vps.assigned = True
                        vps.save()

                        account.balance = Decimal(account.balance) - Decimal(template.cost)
                        account.save()
                        log = AccountLogs.objects.create(
                            description="Generated",
                            account=account,
                            amount=Decimal(template.cost) * -1,
                            balance=account.balance,
                            instance=vps,

                        )
                        log.save()
                        usage = Usage(
                            instance=vps,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        vps.current_usage = usage
                        vps.save()
                messages.success(request, f'Generated proxies. Please contact the Administrator to generate more')
            else:
                messages.success(request, f'Your account balance not enough')
            

    return redirect(reverse('superuser_home'))

from utils.ssh import update_instance_through_ssh
@login_required
def seller_generate_instance(request, pk):
    if request.method == "POST":
        auto = request.POST.get('auto')
        seller_template = SellerTemplates.objects.get(id=pk)
        # number_of_instances = int(seller_template.quantity)
        number_of_instances = int(1)
        template = Templates.objects.get(id=seller_template.template.id)
        if template.generation == 'auto':
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            if account.balance >= (Decimal(seller_template.cost) * Decimal(int(number_of_instances))):
                client = get_client(template, request.user, VPS)
                # key = generate_key(client, template, request.user)
                # print(key)
                print("GETTTING HERE")
                if template.obj_type == 'vps':
                    # type_ = VPS.objects.filter(Q(obj_type='vps') &Q(user=request.user)).first()
                    response = create_instance(client, template.template_id, number_of_instances, number_of_instances)
                    print(response)
                    try:
                        for instance in response["Instances"]:
                            # instance = response['Instances'][0]
                            instance = instance
                            waiter = client.get_waiter('instance_running')
                            res = waiter.wait(InstanceIds=[instance['InstanceId']])
                            vps = VPS(
                                instance_id= instance['InstanceId'],
                                aws_account=template.aws_account,
                                obj_type = 'vps',
                                state= instance['State']['Name'],
                                created_by=request.user,
                                template=template,
                                date_created=datetime.datetime.now()

                                # key_name=key
                            )
                            vps.save()
                            # waiter = client.get_waiter('instance_running')
                            # res = waiter.wait(InstanceIds=[vps.instance_id])
                            hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()
                            # hostname = vps.update_hostname()
                            print(hostname)
                            # vps.date_generated = date
                            # vps.time_generated = time
                            vps.hostname = hostname
                            vps.port = template.port
                            vps.instance_user = template.user
                            vps.instance_password = template.password
                            vps.summary = summary
                            vps.save()
                            account.balance = Decimal(account.balance) - Decimal(seller_template.cost)
                            account.save()
                            log = AccountLogs.objects.create(
                                description="Generated",
                                account=account,
                                amount=Decimal(seller_template.cost) * -1,
                                balance=account.balance,
                                instance=vps,

                            )
                            log.save()
                            usage = Usage(
                                instance=vps,
                                start_date = datetime.datetime.now()
                            )
                            usage.save()
                            vps.current_usage = usage
                            vps.save()

                            print('Updating SSH')

                            # update_instance_through_ssh(client, template.aws_account, vps)

                    except Exception as e:
                        print(e)
                        messages.error(request, f'Something went wrong Please Contact The Administrator')
                elif template.obj_type == 'proxy':
                    # type_ = VPS.objects.filter(Q(obj_type='proxy') &Q(user=request.user)).first()
                    response = create_instance(client, template.template_id, number_of_instances, number_of_instances)
                    print(response)
                    try:
                        print("Connecting and trying")
                        for instance in response['Instances']:
                            # instance = response['Instances'][0]
                            print(instance)
                            waiter = client.get_waiter('instance_running')
                            res = waiter.wait(InstanceIds=[instance['InstanceId']])
                            vps = VPS(
                                instance_id= instance['InstanceId'],
                                aws_account=template.aws_account,
                                obj_type = 'proxy',
                                state= instance['State']['Name'],
                                created_by=request.user,
                                template=template,
                                date_created=datetime.datetime.now()
                            )
                            vps.save()
                            print('Created Instance')
                            hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()
                            print(hostname)
                            vps.hostname = hostname
                            vps.port = template.port
                            vps.instance_user = template.user
                            vps.instance_password = template.password
                            vps.summary = summary
                            vps.save()
                            account.balance = Decimal(account.balance) - Decimal(seller_template.cost)
                            print("COStttttttttttt")
                            print(seller_template.cost)
                            
                            account.save()
                            log = AccountLogs.objects.create(
                                description="Generated",
                                account=account,
                                amount=Decimal(seller_template.cost) * -1,
                                balance=account.balance,
                                instance=vps
                            )
                            log.save()
                            usage = Usage(
                                instance=vps,
                                start_date = datetime.datetime.now()
                            )
                            usage.save()
                            vps.current_usage = usage
                            vps.save()

                            messages.success(request, f'Successfully created')

                    except Exception as e:
                        print(e)

                        messages.error(request, f'Something went wrong Please Contact The Administrator')
            
            else:
                messages.error(request, f"Your Account does have enough balance to generate the {number_of_instances} instance")
        elif template.generation == 'manual':
            print('PPOOPPPOWPOEPPWOOWPPWPPW')
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            if account.balance >= (Decimal(seller_template.cost) * Decimal(int(number_of_instances))):
                objects = VPS.objects.filter(Q(template=template) & Q(assigned=False))
                if len(objects) == 0:
                    print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
                    messages.success(request, f'Could Not Generate Proxy. Please contact the Administrator to generate more')
                elif len(objects) >= number_of_instances:
                    print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
                    for i in range(number_of_instances):
                        vps = VPS.objects.get(id=objects[i].id)
                        vps.date_created = datetime.datetime.now()
                        vps.created_by = request.user
                        vps.assigned = True
                        vps.save()

                        account.balance = Decimal(account.balance) - Decimal(seller_template.cost)
                        account.save()
                        log = AccountLogs.objects.create(
                            description="Generated",
                            account=account,
                            amount=Decimal(seller_template.cost) * -1,
                            balance=account.balance,
                            instance=vps,

                        )
                        log.save()
                        usage = Usage(
                            instance=vps,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        vps.current_usage = usage
                        vps.save()

                elif len(objects) < number_of_instances:
                    print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf')
                    for i in range(len(objects)):
                        vps = VPS.objects.get(id=i.id)
                        vps.date_created = datetime.datetime.now()
                        vps.created_by = request.user
                        vps.assigned = True
                        vps.save()

                        account.balance = Decimal(account.balance) - Decimal(seller_template.cost)
                        account.save()
                        log = AccountLogs.objects.create(
                            description="Generated",
                            account=account,
                            amount=Decimal(seller_template.cost) * -1,
                            balance=account.balance,
                            instance=vps,

                        )
                        log.save()
                        usage = Usage(
                            instance=vps,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        vps.current_usage = usage
                        vps.save()
                messages.success(request, f'Generated. Please contact the Administrator to generate more')
            else:
                messages.success(request, f'Your account balance not enough')
            
    if request.user.is_superuser:
        return redirect(reverse('superuser_home'))
    elif request.user.is_seller:
        return redirect(reverse('seller'))

from .models import RDPFile
from django.http import Http404, HttpResponse

@login_required
def user_dashboard(request):
    if request.user.is_admin:
        return redirect(reverse('control_panel'))
    if request.user.is_superuser:
        return redirect(reverse('superuser_home'))
    if request.user.is_seller:
        return redirect(reverse('seller'))
    try:
        instance = VPS.objects.get(user=request.user)
    except VPS.DoesNotExist as e:
        raise Http404()
    # if instance.rdp_file == None:
    # instance.generate_rdp()
    context = {
        'instance': instance,
        'status': instance.status(client(instance)),
        'obj':RDPFile.objects.get_or_create(id=1)[0]
    }
    return render(request, 'aberd/user_dashboard.html', context)


@login_required
def superuser_dashboard(request):
    if request.user.is_superuser:
        context = {
            "account": VPS.objects.filter(user=request.user).first(),
            'vpsform': PROXYFORM,
            'proxyform': PROXYFORM,
            'proxies': VPS.objects.filter(Q(template__obj_type='proxy') & Q(deleted=False)).order_by('id'),
            'vpses': VPS.objects.filter(Q(template__obj_type='vps') & Q(deleted=False)).order_by('id'),
        }
        return render(request, 'main/superuser_dashboard.html', context)





import datetime

import random
import string

def random_char(char_num):
       return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))


from allauth.account.models import EmailAddress

@login_required
def superuser_attach_user(request, pk):
    instance = VPS.objects.get(id=pk)
    if request.user.is_superuser or request.user.is_seller:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            password =   request.POST.get('password')
            email =   random_char(10)+"@gmail.com".lower()
            
            filter_user = CustomUser.objects.filter(email=email) 
            if len(filter_user) < 1:
                try:
                    user, new = CustomUser.objects.get_or_create(
                        username = user_id,
                        email = email,
                        is_admin = False,
                        is_superuser = False,
                        is_normal = True,
                        is_active=True
                    )
                    if new:
                        user.set_password(password)
                        user.save()


                        email__ = EmailAddress()
                        email__.email = email
                        email__.user = user
                        email__.verified = True
                        email__.primary = True
                        email__.save()
                        
                        instance.user = user
                        instance.instance_user = user_id
                        instance.user_attached = True
                        instance.instance_password = password
                        instance.save()
                        
                        print("ave User OOOOOOOOO")
                        print("PPPPPPPPPPPPPPPPPPPPPPPPppp")
                        
                        usage = Usage(
                            instance=instance,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        
                        print('saved usage')
                        
                        instance.current_usage = usage
                        instance.save()
                        
                        print("Finished saving")
                        
                
                        

                        return redirect(reverse('vps_history_spu'))
                    else:
                        messages.error(request, 'Username Already Exists')

                    return redirect(reverse('vps_history_spu'))

                except Exception as e:
                    print(e)
                    messages.error(request, f'User Already Exists.')
                    return redirect(reverse('vps_history_spu'))
            else:
                messages.error(request, 'User with that Email Already Exists')
                return redirect(reverse('vps_history_spu'))

@login_required
def instance_details(request, pk):
    instance = VPS.objects.get(id=pk)
    context = {
        "instance": instance
    }
    return render(request, 'main/instance_details.html')

from .models import Usage
@login_required
def user_action_form(request):
    if request.method == 'POST':
        status = ''
        button = request.POST.get('button')

        intance_id = request.POST.get('id')
        instance = VPS.objects.get(instance_id=intance_id)
        print(request.POST)
        status = ''
        description = instance.status(client(instance))


        if button == 'Start':
            if description.lower() == "running":
                messages.error(request, f'Instance is running')
            else:
                try:
                    status = instance.start(client(instance))
                    usage = Usage(
                        instance=instance,
                        start_date = datetime.datetime.now(tz=timezone.utc)
                    )
                    usage.save()
                    instance.current_usage = usage
                    instance.save()
                except KeyError as e:
                    messages.error(request, f'Failed. Try Again')
                return redirect(reverse('user_dashboard'))

        if button == 'Stop':
            if description.lower() == "stopped":
                messages.error(request, f'Instance is already stopped')

                usage_ = instance.current_usage
                utz=pytz.UTC
                usage_.stop_date = datetime.datetime.now(tz=timezone.utc)
                usage_.description = request.user.username
                usage_.save()

                instance.current_usage = None
                instance.save()
            else:
                usage = instance.current_usage
                try:
                    status = instance.stop(client(instance))
                    print('RTTTTEE')
                    utz=pytz.UTC
                    usage.stop_date = datetime.datetime.now(tz=timezone.utc)
                    usage.description = request.user.username
                    usage.save()

                    print('RTTTTEE')
                    instance.current_usage = None
                    instance.save()
                    print('RTTTTEE')
                except KeyError as e:
                    messages.error(request, f'Failed. Try Again')

                messages.error(request, f'The operation { status }')
                return redirect(reverse('user_dashboard'))
    return redirect(reverse('user_dashboard'))



@login_required
def stop(request):
    if request.method == 'POST':
        id = request.method.POST.get('id')
        template = Templates.objects.filter(instance_id=id)
        client = get_session(template, request.user, VPS)
        try:
            response = client.stop_instances(InstanceIds=[id])
            print('Success', response)
            messages.success(request, 'Instance Stopped Successfully')

        except ClientError as e:
            print('Error', e)
    return render(request, 'main/user_dashboard.html')

@login_required
def update_time(request):
    if request.method == 'POST':
        hours = request.method.POST.get('hours')
        days = request.method.POST.get('days')
        usage = request.method.POST.get('usage')
        instance = VPS.objects.filter(user=request.user).first()
        instance.hours = int(hours)
        instance.days = int(days)
        instance.usage = int(usage)
        instance.save()
        messages.success(request, 'Update Successful')
    return render(request, 'main/user_dashboard.html')





@login_required
def superuser_add_vps(request):
    if request.user.is_admin:
        if request.method == 'POST':
            aws_account_id = request.POST.get('aws_account_id')
            user_id = request.POST.get('user_id')
            password =   request.POST.get('password')

            user, new = CustomUser.objects.get_or_create(
                username = user_id,
                is_active=True
            )
            user.set_password(password)
            user.save()
            vps  = VPS(
                sub_type='vps',
                user=user,
                days=0,
                hours=0,
                usage=0,
                password=password,
                aws_account_id=aws_account_id,
                created_by=request.user,
                date_created=datetime.datetime.now()


            )
            vps.save()
        return redirect(reverse('superuser_dashboard'))
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect('/login')




@login_required
def superuser_add_proxy(request):
    if request.user.is_admin:
        if request.method == 'POST':
            aws_account_id = request.POST.get('aws_account_id')
            user_id = request.POST.get('user_id')
            password =   request.POST.get('password')

            user, new = CustomUser.objects.get_or_create(
                username = user_id,
                is_active=True
            )
            user.set_password(password)
            user.save()
            vps  = VPS(
                sub_type='proxy',
                user=user,
                password=password,
                aws_account_id=aws_account_id,
                created_by=request.user,
                date_created=datetime.datetime.now()

            )
            vps.save()
        return redirect(reverse('superuser_dashboard'))
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect('/login')



@login_required
def templates(request):
    if request.user.is_admin:
        context = {
            'templates': Templates.objects.all(),
    
        }
        return render(request, 'main/templates.html', context)


@login_required
def templates_add(request):
    if request.user.is_admin:
        if request.method == "POST":
            print("OOOOOOOOOOOOOOOOOOOOOOOOOO")
            print(request.POST)
            form = TemplateFORM(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.created_by = request.user
                data.save()
                return redirect(reverse('templates'))
            messages.error(request, form.errors)
        context = {
            'templateForm': TemplateFORM,
        }
        return render(request, 'main/template_add.html', context)

import datetime

@login_required
def templates_edit(request, pk):
    if request.user.is_admin:
        if request.method == "POST":


            print(request.POST)
            form = TemplateFORM(request.POST, instance=Templates.objects.get(id=pk))
            if form.is_valid():
                data = form.save(commit=False)
                data.modified_by = request.user
                data.date_modified = datetime.datetime.now()
                data.save()

                return redirect(reverse('templates'))
            messages.error(request, form.errors)
        context = {
            'templateForm': TemplateFORM(instance=Templates.objects.get(id=pk)),
            'template': Templates.objects.get(id=pk)
        }
        return render(request, 'main/template_edit.html', context)















from .models import AwsAccounts


@login_required
def aws_accounts(request):
    if request.user.is_admin:
        context = {
            'accounts': AwsAccounts.objects.all(),
    
        }
        return render(request, 'main/aws_accounts.html', context)


@login_required
def aws_account_add(request):
    if request.user.is_admin:
        if request.method == "POST":
            form = AwsAccountsFORM(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.created_by = request.user
                data.save()

                return redirect(reverse('aws_accounts'))
            messages.error(request, form.errors)
        context = {
            'accountForm': AwsAccountsFORM,
        }
        return render(request, 'main/aws_account_add.html', context)

import datetime

@login_required
def aws_account_edit(request, pk):
    if request.user.is_admin:
        if request.method == "POST":
            form = AwsAccountsFORM(request.POST, request.FILES, instance=AwsAccounts.objects.get(id=pk))
            print(request.POST)
            print(request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                try:
                    data.ssh_key = request.FILES['ssh_key']
                except Exception as e:
                    pass
                data.modified_by = request.user
                data.date_modified = datetime.datetime.now()
                data.save()
                return redirect(reverse('aws_accounts'))
            messages.error(request, form.errors)
        context = {
            'accountForm': AwsAccountsFORM(instance=AwsAccounts.objects.get(id=pk)),
            'account': AwsAccounts.objects.get(id=pk)
        }
        return render(request, 'main/aws_account_edit.html', context)























from .forms import CSVFIleForm
from .models import CsvFile
from itertools import chain
@login_required
def control_panel(request):
    vpses = len(VPS.objects.filter(Q(obj_type='vps') & Q(created_by__is_superuser=True) & Q(deleted=False))) + len(VPS.objects.filter(Q(obj_type='vps') & Q(created_by__is_seller=True) & Q(deleted=False)))
   
    man_proxies = len(VPS.objects.filter(Q(obj_type='proxy') & Q(template__generation='manual') & Q(deleted=False) & Q(assigned=False)))
  
    proxies = len(VPS.objects.filter(Q(obj_type='proxy') & Q(created_by__is_superuser=True) & Q(deleted=False))) + len(VPS.objects.filter(Q(obj_type='proxy') & Q(created_by__is_seller=True) & Q(deleted=False)))
   
    if request.user.is_admin:
        context = {
            'files': CsvFile.objects.all(),
            'csvform': CSVFIleForm,
            'vpsform': SuperUserVPSAccountForm,
            'proxyform': SuperUserPROXYAccountForm,
            'manual_proxyform': ManualSuperUserPROXYAccountForm,
            'proxies': proxies,
            'man_proxies': man_proxies,
            'vpses': vpses,
            'users': len(CustomUser.objects.filter(Q(is_superuser=True) & Q(deleted=False))) - 1
        
        }
        return render(request, 'aberd/home.html', context)
    logout(request)
    messages.success(request, 'You do not have permission to view. Session Closed') 
    return redirect('/login')
    # return render(request, 'main/usage.html', context)



@login_required
def control_panel_vps(request):

    if request.method == 'POST':
        print("GETTTTTTT")
        print(request.POST)
        form = SuperUserVPSAccountForm(request.POST)
        if form.is_valid():
            print("PPPPPPPPPPPP")
            form.obj_type = 'vps'
            obj = form.save(commit=False)
            print("RRRRRRRRRRRRRRR")
            
            obj.save()

    return redirect(reverse('vps_view_summary_control_panel'))



@login_required
def control_panel_proxy(request):
    if request.user.is_admin:
        if request.method == 'POST':
            aws_account_id = request.POST.get('aws_account_id')
            user_id = request.POST.get('user_id')
            password =   request.POST.get('password')
            account =   request.POST.get('aws_account')
            account = AwsAccounts.objects.get(id=account)

            user = CustomUser.objects.filter(username=user_id)
            if user.count() > 0:
                user = user.first()
            else:
                user, new = CustomUser.objects.get_or_create(
                    username = user_id,
                    is_superuser=True,
                    is_active=True
                )
                user.set_password(password)
                user.save()
  
            #check for instances
            instances = VPS.objects.filter(Q(user=user) & Q(obj_type='proxy'))
            if instances.count() > 0:
                messages.error(request, 'This User Has A Proxy Associated Already')
                return redirect(reverse('proxy_view_summary'))
            vps  = VPS(
                obj_type='proxy',
                user=user,
                password=password,
                aws_account=account,
                date_created=datetime.datetime.now()

            )
            vps.save()
        return redirect(reverse('proxy_view_summary'))
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect('/login')


from utils.route53 import update_route53
@login_required
def manual_proxy_add_control_panel_proxy(request):
    if request.user.is_admin:
        if request.method == 'POST':
            template = request.POST.get('template')
            summary = request.POST.get('summary')
            template = Templates.objects.get(id=template)
            vps  = VPS(
                obj_type='proxy',
                template=template,
                summary = summary,
                date_created=datetime.datetime.now()
            )
            vps.save()
            #update route 53
            try:
                res = update_route53(template, summary)
                if res == True:
                    print(res)
                    messages.success(request, 'Dns Update Successfull') 
                else:
                    messages.error(request, 'Could Not Update Dns') 
            except ClientError as e:
                messages.error(request, 'Could Not Update Dns') 
        return redirect(reverse('manual_proxy'))
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect('/login')


@login_required
def add_credit(request):
    if request.user.is_admin or request.user.is_superuser:
        if request.method == 'POST':
            aws_account_id = request.POST.get('aws_account_id')
            amount = request.POST.get('amount')
            # instance = VPS.objects.get(id=aws_account_id)
            user = CustomUser.objects.get(id=aws_account_id)

            print(request.POST)
            account, new = Accounts.objects.get_or_create(
                user=user,
            )

            # clear logs
            logs = AccountLogs.objects.filter(account=account)
            logs.delete()
            account.balance = Decimal(account.balance) + Decimal(amount)
            account.save()

            log = AccountLogs.objects.create(
                description="Add Credit",
                account=account,
                amount=Decimal(amount),
                balance=account.balance,
                # instance=instance
            )
            log.save()
            # account = VPS.objects.filter(id=aws_account_id).first()
            # account.balance = account.balance + Decimal(amount)
            # account.save()
            messages.success(request, f'Success. Add Credit For New Balance {account.balance}')
        if request.user.is_admin:
            return redirect(reverse('control_panel'))
        elif request.user.is_superuser:
            return redirect(reverse('superuser_home'))
        else:
            logout(request)
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect(reverse('control_panel'))


@login_required
def add_seller_credit(request):
    if request.user.is_admin or request.user.is_superuser:
        if request.method == 'POST':
            aws_account_id = request.POST.get('aws_account_id')
            amount = request.POST.get('amount')

            #get superuser account
            su_account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            
            if su_account.balance > Decimal(amount):
                su_account.balance = Decimal(su_account.balance) - Decimal(amount)
                su_account.save()

                su_log = AccountLogs.objects.create(
                    description="Seller Credit Deducted",
                    account=su_account,
                    amount=Decimal(amount),
                    balance=su_account.balance,
                )
                su_log.save()

                user = CustomUser.objects.get(id=aws_account_id)
                print(request.POST)
                account, new = Accounts.objects.get_or_create(
                    user=user,
                )

                # clear logs
                logs = AccountLogs.objects.filter(account=account)
                logs.delete()
                account.balance = Decimal(account.balance) + Decimal(amount)
                account.save()

                log = AccountLogs.objects.create(
                    description="Add Credit",
                    account=account,
                    amount=Decimal(amount),
                    balance=account.balance,
                    # instance=instance
                )
                log.save()
                # account = VPS.objects.filter(id=aws_account_id).first()
                # account.balance = account.balance + Decimal(amount)
                # account.save()
                messages.success(request, f'Success. Add Credit For New Balance {account.balance}')
        if request.user.is_admin:
            return redirect(reverse('control_panel'))
        elif request.user.is_superuser:
            return redirect(reverse('superuser_home'))
        else:
            logout(request)
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect(reverse('superuser_home'))

@login_required
def account(request, pk):
    print('GETTING HERE')
    user = CustomUser.objects.get(id=pk)
    account, new = Accounts.objects.get_or_create(user=user)
    print('GETTING HERE')

    if request.user.is_admin or account.user == request.user:

        logs = AccountLogs.objects.filter(account=account).order_by('date')
        context = {
            'account': account,
            'logs': logs
        }
        print('GETTITTTTTTTTTTTTTTTTTTTTTTTTTTTTt')

        return render(request, 'main/account.html', context)
    if request.user.is_admin:
        return redirect(reverse('control_panel'))
    elif request.user.is_superuser:
        return redirect(reverse('superuser_home'))
    else:
        return redirect(reverse('user_dashboard'))


@login_required
def usage(request, pk):
    print('GETTING HERE')
    order = OrderDetail.objects.get(id=pk)
    instance = order.instance

    logs = Usage.objects.filter(instance=instance)
    context = {
        'instance': instance,
        'logs': logs
    }

    return render(request, 'main/usage.html', context)

@login_required
def usage_delete(request, pk):
    logs = Usage.objects.get(id=pk)
    instance_id = logs.instance.id
    logs.delete()
    return redirect(reverse('usage', args=(instance_id,) ))

@login_required
def admin_terminate(request, pk):
    if request.method == 'POST':
        id = request.method.POST.get('id')
        template = Templates.objects.filter(instance_id=id)
        client = get_session(template, request.user, VPS)
        try:
            response = client.stop_instances(InstanceIds=[id])
            print('Success', response)
            message.success(request, 'Instance Stopped Successfully')

        except ClientError as e:
            print('Error', e)
    return redirect(reverse('control_panel'))
@login_required
def admin_renew(request, pk):
    if request.method == 'POST':
        id = request.method.POST.get('id')
        instance = Templates.objects.filter(instance_id=id)
        client = get_session(template, request.user, VPS)
        try:
            response = client.stop_instances(InstanceIds=[id])
            print('Success', response)
            message.success(request, 'Instance Stopped Successfully')

        except ClientError as e:
            print('Error', e)
    return redirect(reverse('control_panel'))
@login_required
def proxy_terminate(request, pk):
    if request.method == 'POST':
        id = request.method.POST.get('id')
        instance = Templates.objects.filter(instance_id=id)
        client = get_session(template, request.user, VPS)
        try:
            response = client.stop_instances(InstanceIds=[id])
            print('Success', response)
            message.success(request, 'Instance Stopped Successfully')

        except ClientError as e:
            print('Error', e)
    return redirect(reverse('control_panel'))
















@login_required
def superuser_terminate(request, pk):
    if request.method == 'POST':
        id = request.method.POST.get('id')
        template = Templates.objects.filter(instance_id=id)
        client = get_session(template, request.user, VPS)
        try:
            response = client.stop_instances(InstanceIds=[id])
            print('Success', response)
            message.success(request, 'Instance Stopped Successfully')

        except ClientError as e:
            print('Error', e)
    return redirect(reverse('superuser_home'))
@login_required
def superuser_renew(request, pk):
    if request.method == 'POST':
        id = request.method.POST.get('id')
        instance = Templates.objects.filter(instance_id=id)
        client = get_session(template, request.user, VPS)
        try:
            response = client.stop_instances(InstanceIds=[id])
            print('Success', response)
            message.success(request, 'Instance Stopped Successfully')

        except ClientError as e:
            print('Error', e)
    return redirect(reverse('superuser_home'))
@login_required
def superuser_proxy_terminate(request, pk):
    if request.method == 'POST':
        id = request.method.POST.get('id')
        instance = Templates.objects.filter(instance_id=id)
        client = get_session(template, request.user, VPS)
        try:
            response = client.stop_instances(InstanceIds=[id])
            print('Success', response)
            message.success(request, 'Instance Stopped Successfully')

        except ClientError as e:
            print('Error', e)
    return redirect(reverse('control_panel'))

from utils.ec2 import client
from main.models import Templates
@login_required
def delete_vps(request, pk, page):
    user = ''
    instance = VPS.objects.get(id=pk)
    obj_type = 'vpn'
    if instance.obj_type == 'vpn':
        obj_type = instance.obj_type
        instance.delete()
        print(request.path)
    else:
        obj_type = instance.template.obj_type
        # if request.user.is_admin or request.user == order.customer:
        try:
            
            # instance = order.instance
            user = instance.user
            if user is not None:
                if not user.is_superuser and not user.is_admin:
                    user = CustomUser.objects.get(id=user.id)
                    
            if instance.template.generation == 'manual':
                pass
            else:
                c = client(instance)
                try:
                    c.terminate_instances(InstanceIds=[instance.instance_id])
                except ClientError  as e:
                    if request.user.is_admin:
                        messages.error(request, f'Instance {instance.instance_id} Not Available On AWS ACCOUNT { instance.aws_account.account_id}')
                    else:
                        pass
            instance.current_usage = None
            instance.save()

            usage = Usage.objects.filter(instance=instance)
            usage.delete()
            
            logs = AccountLogs.objects.filter(instance=instance)
            for log in logs:
                lo = AccountLogs.objects.get(id=log.id)
                lo.instance = None
                lo.save()
            instance.delete()
            if user is not None:
                if not user.is_superuser and not user.is_admin:
                    user.delete()
            messages.error(request, f"Successfully Deleted")

        except Exception as e:
            if request.user.is_admin:
                messages.error(request, f"Could Not Delete The Instance")
            else:
                messages.error(request, f"Could Not Delete. Please Contact The Administrator")
                
    # path_info = request.path_info.split("/")[-1]
    # if path_info != "":
    #     return redirect(reverse(f'{path_info}'))
    
        
    if str(page) == "1":
        return redirect(reverse('vps_view_summary_control_panel'))
    
    if str(page) == "2":
        return redirect(reverse('proxy_view_summary'))
    
    if str(page) == "3":
        return redirect(reverse('manual_proxy'))
    
    if str(page) == "4":
        return redirect(reverse('vpn_view_summary'))
    
    if str(page) == "5":
        return redirect(reverse('manual_vpn'))

    if not request.user.is_admin:
        if obj_type == 'vps':
            return redirect(reverse('vps_history_spu'))
        
        elif obj_type == 'vpn':
            return redirect(reverse('vpn_history_spu'))
        
        elif obj_type == 'proxy':
            return redirect(reverse('proxies_history_spu'))
        
        else:
            return redirect(reverse('superuser_home'))
    else:
        if obj_type == 'vps':
            return redirect(reverse('vps_view_summary_control_panel'))
        
        elif obj_type == 'vpn':
            return redirect(reverse('vpn_view_summary'))
        
        elif obj_type == 'proxy':
            return redirect(reverse('proxy_view_summary'))
        
        else:
            return redirect(reverse('control_panel'))

@login_required
def delete_user(request, pk):

    print("Deleting User TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTtttt")
        
    try:
        user = CustomUser.objects.get(id=pk)
        
        templates = Templates.objects.filter(super_user__id__in=[user.id,])
        for template in templates:
            template.super_user.remove(user)
            template.save()
        orders = OrderDetail.objects.filter(customer=user)
            
        orders.delete()
        print(user)
        try:
            instances = VPS.objects.filter(created_by=user)
            users_ = CustomUser.objects.filter(id__in=[ ins.user.id for ins in instances])
            for instance in instances:
                ins = VPS.objects.get(id=instance.id)
                ins.current_usage = None
                ins.save()
                try:
                    client = get_client(instance.template, request.user, VPS)
                    try:
                        client.terminate_instances(InstanceIds=[instance.instance_id])
                    except ClientError as e:
                        messages.error(request, 'Resource Could not be found')
                except AttributeError  as e:
                    pass
                ins.user = None
                ins.delete()

                logs = AccountLogs.objects.filter(instance=ins)
                for log in logs:
                    lo = AccountLogs.objects.get(id=log.id)
                    lo.instance = None
                    lo.created_by=None
                    lo.save()

            account = Accounts.objects.get(user=user)
            logs = AccountLogs.objects.filter(account=account)
            logs.delete()
            account.delete()
            users_.delete()
            instances.delete()
            user.deleted = True
            templates = Templates.objects.filter(super_user=user)
            for template in templates:
                t = Template.objects.get(id=template.id)
                t.super_user = None
                t.save()

            instances = VPS.objects.filter(user=user)
            instances.delete()
            user.delete()
        except Exception as e:
            user.delete()
        
            
        if request.user.is_admin:
            return redirect(reverse('superuser_accounts'))

        if request.user.is_superuser:
            return redirect(reverse('superuser_accounts'))

    except Exception as e:
        print(e)
        messages.error(request, f"Could Not Delete {user.username}. Other resources are associated with this user")

        if request.user.is_admin:
            return redirect(reverse('superuser_accounts'))

        if request.user.is_superuser:
            return redirect(reverse('superuser_accounts'))






@login_required
def delete_user_accounts(request, pk):

    print("Deleting User TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTtttt")
        
    try:
        user = CustomUser.objects.get(id=pk)
        
        templates = Templates.objects.filter(super_user__id__in=[user.id,])
        for template in templates:
            template.super_user.remove(user)
            template.save()
        orders = OrderDetail.objects.filter(customer=user)
            
        orders.delete()
        print(user)
        try:
            instances = VPS.objects.filter(created_by=user)
            users_ = CustomUser.objects.filter(id__in=[ ins.user.id for ins in instances])
            for instance in instances:
                ins = VPS.objects.get(id=instance.id)
                ins.current_usage = None
                ins.save()
                try:
                    client = get_client(instance.template, request.user, VPS)
                    try:
                        client.terminate_instances(InstanceIds=[instance.instance_id])
                    except ClientError as e:
                        messages.error(request, 'Resource Could not be found')
                except AttributeError  as e:
                    pass
                ins.user = None
                ins.delete()

                logs = AccountLogs.objects.filter(instance=ins)
                for log in logs:
                    lo = AccountLogs.objects.get(id=log.id)
                    lo.instance = None
                    lo.created_by=None
                    lo.save()

            account = Accounts.objects.get(user=user)
            logs = AccountLogs.objects.filter(account=account)
            logs.delete()
            account.delete()
            users_.delete()
            instances.delete()
            user.deleted = True
            templates = Templates.objects.filter(super_user=user)
            for template in templates:
                t = Template.objects.get(id=template.id)
                t.super_user = None
                t.save()

            instances = VPS.objects.filter(user=user)
            instances.delete()
            user.delete()
        except Exception as e:
            user.delete()
        
            
        if request.user.is_admin:
            return redirect(reverse('user_accounts'))

        if request.user.is_superuser:
            return redirect(reverse('user_accounts'))

    except Exception as e:
        print(e)
        messages.error(request, f"Could Not Delete {user.username}. Other resources are associated with this user")

        if request.user.is_admin:
            return redirect(reverse('user_accounts'))

        if request.user.is_superuser:
            return redirect(reverse('user_accounts'))







@login_required
def templates_delete(request, pk):
    template = Templates.objects.get(id=pk)
    try:
        template_name = template.template_name
        
        orders = OrderDetail.objects.filter(package__template=template)
        orders.delete()
        
        instances = VPS.objects.filter(template=template)
        instances.delete()
        
        packages = Packages.objects.filter(template=template)
        packages.delete()
        
        template.delete()
        messages.error(request, f"Successfully Deleted {template_name}.")
        return redirect(reverse('templates'))
    except Exception as e:
        print(e)
        messages.error(request, f"Could Not Delete {template.template_name}. Other resources are associated with this Template")
        return redirect(reverse('templates'))























@login_required
def update_usage(request):
    if request.method == 'POST':
        days = request.POST.get('days')
        hours = request.POST.get('hours')
        usage = request.POST.get('usage')
        instance = VPS.objects.get(user=request.user)
        instance.days = int(days)
        instance.hours = int(hours)
        instance.usage = int(usage)
        instance.save()        
    return redirect(reverse('user_dashboard'))






@login_required
def instance_renew(request, pk):
    instance = VPS.objects.get(id=pk)
    if request.user.is_admin:
        account, new = Accounts.objects.get_or_create(
            user=instance.created_by,
        )
        if account.balance >= instance.template.cost:
            account.balance = Decimal(account.balance) - Decimal(instance.template.cost)
            account.save()
            log = AccountLogs.objects.create(
                description="Renew",
                account=account,
                amount=Decimal(instance.template.cost) * -1,
                balance=account.balance,
                instance=instance,
                created_by=request.user
            )
            log.save()

            instance.date_created = datetime.datetime.now()
            instance.save()

            usage = Usage.objects.filter(instance=instance)
            usage.delete()
            
            # usage = Usage(
            #     instance=instance,
            #     start_date = datetime.datetime.now()
            # )
            # usage.save()
            instance.current_usage = None
            instance.save()
        else:
            messages.error(request, "Account does have enough balance to generate the instance")
        return redirect(reverse('control_panel'))

    if request.user.is_superuser:
        instance = order.instance
        account, new = Accounts.objects.get_or_create(
            user=request.user,
        )
        if account.balance >= instance.template.cost:
            account.balance = Decimal(account.balance) - Decimal(instance.template.cost)
            account.save()
            log = AccountLogs.objects.create(
                description="Renew",
                account=account,
                amount=Decimal(instance.template.cost) * -1,
                balance=account.balance,
                instance=instance,
                created_by=request.user
            )
            log.save()

            instance.date_created = datetime.datetime.now()
            instance.save()

            instance.current_usage = None
            instance.save()

            usage = Usage.objects.filter(instance=instance)
            usage.delete()

            # usage = Usage(
            #     instance=instance,
            #     start_date = datetime.datetime.now()
            # )
            # usage.save()
            # instance.current_usage = usage
            # instance.save()
        else:
            messages.error(request, "Your Account does have enough balance to generate the instance")
        return redirect(reverse('superuser_home'))


@login_required
def instance_terminate(request, pk):
    instance = VPS.objects.get(id=pk)
    account, new = Accounts.objects.get_or_create(
        user=request.user,
    )
    if account.balance >= instance.template.cost:
        account.balance = Decimal(account.balance) - Decimal(template.cost)
        account.save()
        log = AccountLogs.objects.create(
            description="Generated",
            account=account,
            amount=Decimal(template.cost) * -1,
            balance=account.balance,
            instance=vps,
            created_by=request.user
        )
        log.save()
    else:
        messages.error(request, "Your Account does have enough balance to generate the instance")
  
    if request.user.is_admin:
        return redirect(reverse('control_panel'))

    if request.user.is_superuser:
        return redirect(reverse('superuser_home'))

from main.models import PaymentPic
@login_required
def make_payment(request):
    context = {
        "obj": PaymentPic.objects.get_or_create(id=1)[0]
    }
    return render(request, 'aberd/make_payment.html', context)


from utils.ec2 import client
@login_required
def quick_terminate(request):
    user = ''
    instance = VPS.objects.get(id=2)
    c = client(instance)
    response = c.describe_instances(InstanceIds=['i-0b0e836eccc2af311'])

    return JsonResponse(response)

from django.core.mail import send_mail
from django.conf import settings
def contactUs(request):
    print("GETTING HERE")
    print(request.POST)
    if request.method == "POST":
        print('POOSSIISOSOSOSO')
        name = request.POST.get('full_name')
        phone = request.POST.get('phone_number')
        email = request.POST.get('email_address')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        context =  f'{name} of {phone} and email {email} contacted you about {subject}. Detailed message {message}'
        print(context)

        try:
            print('GETTTING HERE')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER,]
            status = send_mail(subject, context, settings.EMAIL_HOST_USER, recipient_list)
            print(status)
            messages.success(request, "Request received. We will get back to you.")

        except Exception as e:
            print(e)

            messages.success(request, "Failed. Please try again.")

    return redirect(reverse('index'))
  

@login_required
def proxy_details(request, pk):
    instance = VPS.objects.get(id=pk)
    if request.method == "POST":
        details = request.POST.get('details')
        instance.proxy_details = details
        instance.proxy_details_set = True
        instance.save()
        messages.error(request, "Update Successfull")
  
    if instance.template.obj_type == 'vps':
        return redirect(reverse('vps_history_spu'))
    
    elif instance.template.obj_type == 'vpn':
        return redirect(reverse('vpn_history_spu'))
    
    elif instance.template.obj_type == 'proxy':
        return redirect(reverse('proxies_history_spu'))
    
    else:
        return redirect(reverse('superuser_home'))



@login_required
def update_time(request, pk, page):
    instance = VPS.objects.get(id=pk)
    if request.method == "POST":
        date = request.POST.get('date')
        instance.date_created = date
        instance.save()
        messages.error(request, "Update Successfull")
        
        
    if str(page) == "1":
        return redirect(reverse('vps_view_summary_control_panel'))
    
    if str(page) == "2":
        return redirect(reverse('proxy_view_summary'))
    
    if str(page) == "3":
        return redirect(reverse('manual_proxy'))
    
    if str(page) == "4":
        return redirect(reverse('manual_proxy'))
  
    if request.user.is_admin:
        return redirect(reverse('control_panel'))

    if request.user.is_superuser:
        return redirect(reverse('superuser_home'))



@login_required
def update_password(request, pk):
    user = CustomUser.objects.get(id=pk)
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(user)
    print(request.POST)
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        superuser = request.POST.get('superuser')
        print(username, password)

        if username != "":
            user.username = username
            user.save()
            messages.error(request, "Username Update Success")
            
        if superuser == "on":
            user.is_marketer = True
            user.save()
            messages.error(request, "Username Update Success")

        instances = VPS.objects.filter(created_by__id=user.id)
        if password != "":
            user.set_password(password)
            user.first_name = password
            user.save()

            try:
                i = instances[0]
                i.password = password
                i.save()
            except Exception as e:
                pass
            print(instances)

            messages.error(request, "Password Update Success")
    if request.user.is_admin:
        return redirect(reverse('user_accounts'))
  
    if request.user.is_admin:
        return redirect(reverse('control_panel'))

    if request.user.is_superuser:
        return redirect(reverse('superuser_home'))
    
    
    
    
@login_required
def update_password_superuser(request, pk):
    user = CustomUser.objects.get(id=pk)
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(user)
    print(request.POST)
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        superuser = request.POST.get('superuser')
        print(username, password)

        if username != "":
            user.username = username
            user.save()
            messages.error(request, "Username Update Success")
            
        if superuser != "on":
            user.is_marketer = False
            user.save()

        instances = VPS.objects.filter(created_by__id=user.id)
        if password != "":
            user.set_password(password)
            user.first_name = password
            user.save()

            try:
                i = instances[0]
                i.password = password
                i.save()
            except Exception as e:
                pass
            print(instances)

            messages.error(request, "Password Update Success")
    if request.user.is_admin:
        return redirect(reverse('superuser_accounts'))
  
    if request.user.is_admin:
        return redirect(reverse('control_panel'))

    if request.user.is_superuser:
        return redirect(reverse('superuser_home'))

from django.http import HttpResponse, HttpResponseNotFound
import io
from django.conf import settings
import os
@login_required
def download_rdp(request, pk):
    try:
        instance = VPS.objects.get(id=pk)
    except VPS.DoesNotExist as e:
        messages.error(request, "Instance Doesnot Exist")
        return redirect(reverse('user_dashboard'))
        
    try:
        obj = RDPFile.objects.get(id=1)
    except RDPFile.DoesNotExist as e:
        messages.error(request, "Resource Doesnot Exist")
        return redirect(reverse('user_dashboard'))

    try:
        
        file_ = open(obj.rdp_file.path,'r', encoding="utf-16")
        print(obj.rdp_file.path)
        lines = file_.readlines()

        output_path = os.path.join(settings.BASE_DIR, "media/{}.rdp".format(instance.instance_id))
        print(output_path)
        lines[1] = 'full address:s:' + '{}\n'.format(instance.hostname)
        f = io.open(output_path, "w", encoding="utf-16")
        for lin in range(len(lines)):
            f.write(lines[lin])
        f.close()
        filename = "{}.rdp".format(request.user.username)
        data = None
        with open(output_path, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong. Please contact the administrator")
        return redirect(reverse('user_dashboard'))





import boto3
from .forms import CSVFIleForm
@login_required
def upload_csv(request):
    context = {}
    if request.method == "POST":
        if request.user.is_admin:
            print(request.POST)
            print(request.FILES)
            form = CSVFIleForm(request.POST, request.FILES)
            region = 'ap-south-1'
            if form.is_valid():
                data = form.save()
                session = boto3.Session(
                    aws_access_key_id="AKIAYJPNBQCG6RDWDGWO",
                    aws_secret_access_key="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",
                    region_name=region
                )
                s3 = session.resource('s3')
                bucket = 'manual-proxy'

                file = request.FILES['csv_file']
                print(data.csv_file.path)
                data = open(data.csv_file.path, 'r', encoding="utf-8")
                r = data.read()
                print(r)
                print("Data Datatatatatatatatat")
                print(data.read())
                decoded_file = data.read()
                print(decoded_file)
                
                object = s3.Object(bucket, 'upload.csv')

                result = object.put(Body=r)
                
                #result = s3.Bucket(bucket).upload_file(data.csv_file.path,'upload.csv')
                #result = s3.meta.client.put_object(Body=r, Bucket=bucket, Key='filename.csv')

                print(result)
                messages.success(request, 'Upload Successful')
                return redirect(reverse('upload_csv'))
            messages.error(request, form.errors)
        return redirect(reverse('upload_csv'))
    
    context = {
        'files': CsvFile.objects.all(),
        'csvform': CSVFIleForm 
        }
    return render(request, 'aberd/upload_csv.html', context)
        
        
        
        
        
        
        
from .models import CsvFile    
@login_required
def delete_file(request, pk):
    if request.user.is_admin:
        try:
          csv = CsvFile.objects.get(id=pk)
          csv.delete()
          messages.success(request, 'Delete Successful')
          return redirect(reverse('control_panel'))
        except Exception as e:
          pass
    messages.error(request, "Delete Failed")
    return redirect(reverse('control_panel'))

from itertools import chain


@login_required
def seller(request):
    if request.user.is_seller:
        context = {
            "account": Accounts.objects.filter(user=request.user).first(),
            'vpsform': PROXYFORM,
            'proxyform': PROXYFORM,
            'proxies': VPS.objects.filter(Q(created_by=request.user) & Q(template__obj_type='proxy') & Q(deleted=False)).order_by('id'),
            'vpses': VPS.objects.filter(Q(created_by=request.user) & Q(template__obj_type='vps') & Q(deleted=False)).order_by('id'),
            'seller_templates': SellerTemplates.objects.filter(created_by=request.user),
            'templates_auto': list(chain( SellerTemplates.objects.filter(~Q(template__generation__in=['manual']) & Q(sellers__in=[request.user, ])), SellerTemplates.objects.filter(~Q(template__generation__in=['manual']) & Q(seller=request.user)) )),
            'templates': list(chain(SellerTemplates.objects.filter(Q(template__generation='manual') & Q(sellers__in=[request.user, ])), SellerTemplates.objects.filter(Q(template__generation='manual') & Q(seller=request.user)))),
        }
        return render(request, 'main/seller.html', context)

from django.db.utils import IntegrityError

@login_required
def add_seller(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST.get('user_id')
            password = request.POST.get('password')
            amount = Decimal(0.00)

            # su_account, new = Accounts.objects.get_or_create(
            #     user=request.user,
            # )
            # if su_account.balance > Decimal(amount):
            try:
                user, new = CustomUser.objects.get_or_create(
                    username = username,
                    is_seller=True,
                    is_active=True,
                )
                if new:
                    user.set_password(password)
                    user.save()
                    
                vps  = VPS(
                    obj_type='vps',
                    user=user,
                    password=password,
                    date_created=datetime.datetime.now(),
                    super_seller=request.user
                )
                vps.save()
            except IntegrityError as e:
                messages.success(request, f'User with that username already exists.') 
                return redirect(reverse('superuser_home'))
            
            # su_account.balance = Decimal(su_account.balance) - Decimal(amount)
            # su_account.save()
            # su_log = AccountLogs.objects.create(
            #     description="Seller Credit Deducted",
            #     account=su_account,
            #     amount=Decimal(amount),
            #     balance=su_account.balance,
            # )
            # su_log.save()


            # account, new = Accounts.objects.get_or_create(
            #     user=user,
            # )
            # # clear logs
            # logs = AccountLogs.objects.filter(account=account)
            # logs.delete()
            # account.balance = Decimal(account.balance) + Decimal(amount)
            # account.save()
            # log = AccountLogs.objects.create(
            #     description="Opening Credit",
            #     account=account,
            #     amount=Decimal(amount),
            #     balance=account.balance,
            #     # instance=instance
            # )
            # log.save()
            messages.success(request, f'Success. Created Seller {username}') 
            # else:
            #     messages.success(request, f'You do not have Enough credit.') 

        return redirect(reverse('superuser_home'))
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect(reverse('control_panel'))





@login_required()
def sell_template_to_sellers(request):
    context = {
        "templates": SellerTemplates.objects.filter(created_by=request.user)
    }
    return render(request, 'aberd/sell_template.html', context)



@login_required()
def admin_sell_templates_to_sellers(request):
    if request.method == "POST":
        form = AdminAvailToSellerForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            obj.created_by = request.user
            obj.date_created = datetime.datetime.now()
            obj.save()
            messages.success(request, f'Template Sold Successfully')
            return redirect(reverse('admin_sell_templates_to_sellers'))
        return render(request, 'main/admin_sell_template.html', {'form':form, 'templates':SellerTemplates.objects.filter(created_by=request.user).order_by('-id')})
    context = {
        'form': AdminAvailToSellerForm(),
        'templates': SellerTemplates.objects.filter(created_by=request.user).order_by('-id')
    }
    return render(request, 'main/admin_sell_template.html', context)

from django.contrib.auth.decorators import login_required,user_passes_test
def admin_user(user):
    return user.is_admin

@login_required()
@user_passes_test(admin_user)
def admin_delete_template(request, pk):
    item = get_object_or_404(SellerTemplates, id=pk)
    item.delete()
    messages.success(request, 'seller template deleted successfully')
    return redirect(reverse('admin_sell_templates_to_sellers'))

@login_required()
def add_sell_template_to_sellers(request):
    if request.method == 'POST':
        form = AvailToSellerForm( request.user.id, request.POST)
        if form.is_valid():
            obj_ = form.save(commit=False)
            obj_.created_by = request.user
            obj_.date_created = datetime.datetime.now()
            obj_.save()
            form.save_m2m()
        template = obj_.template
        
        
        if obj_.seller is not None:
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            # account.balance = Decimal(account.balance) - Decimal(obj_.get_total_cost)
            account.balance = Decimal(account.balance) - Decimal(0.00)
            account.save()
            # log = AccountLogs.objects.create(
            #     description=f"Template For {obj_.seller}",
            #     account=account,
            #     amount= Decimal(0.00),
            #     balance=account.balance,
            #     instance=None,
            # )
            # log.save()
            
            
            account, new = Accounts.objects.get_or_create(
                user=obj_.seller,
            )
            account.balance = Decimal(account.balance) +  Decimal(0.00)
            account.save()
            # log = AccountLogs.objects.create(
            #     description=f"Template For {obj_.seller}",
            #     account=account,
            #     amount= Decimal(0.00),
            #     balance=account.balance,
            #     instance=None,

            # )
            # log.save()
            return redirect(reverse('sell_template_to_sellers'))
        
        for u in obj_.sellers.all():
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            account.balance = Decimal(account.balance) - Decimal(obj_.get_total_cost)
            account.save()
            log = AccountLogs.objects.create(
                description=f"Template For {u}",
                account=account,
                amount=Decimal(obj_.get_total_cost),
                balance=account.balance,
                instance=None,
            )
            log.save()
            
            
            account, new = Accounts.objects.get_or_create(
                user=u,
            )
            account.balance = Decimal(account.balance) + Decimal(obj_.get_total_price)
            account.save()
            log = AccountLogs.objects.create(
                description=f"Template For {u}",
                account=account,
                amount=Decimal(obj_.get_total_price),
                balance=account.balance,
                instance=None,

            )
            log.save()
        
        return redirect(reverse('sell_template_to_sellers'))
    context = {
        'form': AvailToSellerForm( request.user.id)
    }
    return render(request, 'main/add_sell_template.html', context)





@login_required()
def edit_sell_template_to_sellers(request, pk):
    instance = SellerTemplates.objects.get(id=pk)
    if request.method == 'POST':
        form = AvailToSellerForm2(request.user.id, request.POST, instance=instance)
        if form.is_valid():
            obj_ = form.save(commit=False)
            obj_.modified_by = request.user
            obj_.date_modified = datetime.datetime.now()
            obj_.save()
            form.save_m2m()
            
            print(obj_._old_cost)
            print(obj_.cost)
            print(obj_._old_quantity)
            print(obj_.quantity)
            # obj_ = SellerTemplates.objects.get(id=obj_.id)
            new = Decimal(0.00)
            old = Decimal(0.0)
            cost_diff = Decimal(0.0)
            price_diff = Decimal(0.0)
            if obj_._old_cost  != obj_.cost or obj_._old_quantity != obj_.quantity:
                print("omethiong Changed")
                old = obj_._old_cost * obj_._old_quantity
                new = obj_.cost * obj_.quantity
                price_diff = new - old
                
                old = obj_.template.cost * obj_._old_quantity
                new = obj_.template.cost * obj_.quantity
                cost_diff = new - old

            for u in obj_.sellers.all():
                account, new = Accounts.objects.get_or_create(
                    user=request.user,
                )
                account.balance = Decimal(account.balance) - Decimal(cost_diff)
                account.save()
                log = AccountLogs.objects.create(
                    description=f"Template For to {u}",
                    account=account,
                    amount=Decimal(cost_diff),
                    balance=account.balance,
                    instance=None,

                )
                log.save()
                
                
                account, new = Accounts.objects.get_or_create(
                    user=u,
                )
                account.balance = Decimal(account.balance) + Decimal(price_diff)
                account.save()
                log = AccountLogs.objects.create(
                    description=f"Template For to {u}",
                    account=account,
                    amount=Decimal(price_diff),
                    balance=account.balance,
                    instance=None,

                )
                log.save()
                
        return redirect(reverse('sell_template_to_sellers'))
    context = {
        'form': AvailToSellerForm2(request.user.id, instance=instance)
    }
    return render(request, 'main/edit_sell_template.html', context)







@login_required()
def add_templates_to_sellers(request, pk):
    instance = SellerTemplates.objects.get(id=pk)
    if request.method == 'POST':
        form = AvailToSellerForm3(request.user.id, request.POST, instance=instance)
        if form.is_valid():
            cost = request.POST.get('cost')
            quantity = request.POST.get('quantity')
             
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            account.balance = Decimal(account.balance) - Decimal(int(quantity) * Decimal(cost))
            account.save()
            log = AccountLogs.objects.create(
                description=f"Template For to {instance.seller}",
                account=account,
                amount=Decimal(int(quantity) * Decimal(cost)),
                balance=account.balance,
                instance=None,

            )
            log.save()
            
            
            account, new = Accounts.objects.get_or_create(
                user=instance.seller,
            )
            account.balance = Decimal(account.balance) + Decimal(int(quantity) * Decimal(cost))
            account.save()
            log = AccountLogs.objects.create(
                description=f"Template For to {instance.seller}",
                account=account,
                amount=Decimal(int(quantity) * Decimal(cost)),
                balance=account.balance,
                instance=None,

            )
            log.save()
                
        return redirect(reverse('sell_template_to_sellers'))
    context = {
        'form': AvailToSellerForm3(request.user.id, instance=instance)
    }
    return render(request, 'main/add_more_sell_template.html', context)

@login_required()
def delete_sell_template_to_sellers(request, pk):
    instance = SellerTemplates.objects.get(id=pk)
    
    try:
        quantity = instance.quantity
        cost = instance.template.cost
        price = instance.cost
        
        account, new = Accounts.objects.get_or_create(
            user=request.user,
        )
        account.balance = Decimal(account.balance) - Decimal(int(quantity) * Decimal(cost))
        account.save()
        log = AccountLogs.objects.create(
            description=f"Template Deleted For to {instance.seller}",
            account=account,
            amount=Decimal(int(quantity) * Decimal(cost)),
            balance=account.balance,
            instance=None,

        )
        log.save()
        
        
        account, new = Accounts.objects.get_or_create(
            user=instance.seller,
        )
        account.balance = Decimal(account.balance) + Decimal(int(quantity) * Decimal(price))
        account.save()
        log = AccountLogs.objects.create(
            description=f"Template Deleted For to {instance.seller}",
            account=account,
            amount=Decimal(int(quantity) * Decimal(price)),
            balance=account.balance,
            instance=None,

        )
        log.save()
    except Exception as e:
        pass
    instance.delete()
    return redirect(reverse('sell_template_to_sellers'))





@login_required
def update_seller_info(request, pk, id):
    seller = CustomUser.objects.get(id=pk)
    if request.method == "POST":
        print(request.POST)
        quantity = request.POST.get('quantity')
        credit = request.POST.get('credit')
        template = request.POST.get('template')
        
        if template != '' and template != 'Choose Template':
            seller_template = SellerTemplates.objects.get(id=template)
            
            seller_template.sellers.add(seller)
            seller_template.save()
            try:
                seller.seller_template = seller_template
                seller.template = seller_template.template
                seller.save()
            except Exception as e:
                print(e)
            
        if quantity != '' and int(quantity) != 0:
            seller.seller_quantity += int(quantity)
            seller.save()
        
        if credit  != '':
            account = Accounts.objects.get(user=seller)
            account.balance += Decimal(credit)
            account.save()
            log = AccountLogs.objects.create(
                description=f"Template For {seller}",
                account=account,
                amount=Decimal(credit),
                balance=account.balance,
                instance=None,
            )
            log.save()
            account, new = Accounts.objects.get_or_create(
                user=request.user,
            )
            account.balance = Decimal(account.balance) - (Decimal(quantity) * Decimal(seller_template.template.cost))
            account.save()
            log = AccountLogs.objects.create(
                description=f"Template For {seller}",
                account=account,
                amount=Decimal(quantity) * Decimal(seller_template.template.cost),
                balance=account.balance,
                instance=None,
            )
            log.save()
        

        seller.save()
        return redirect(reverse('superuser_home'))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@login_required()
def user_accounts(request):
    context = {
        'users': CustomUser.objects.filter(Q(is_superuser=True) & Q(is_marketer=False) & Q(is_admin=False))
        
    }
    return render(request, 'aberd/usersaccounts.html', context)



@login_required()
def superuser_accounts(request):
    context = {
        'users': CustomUser.objects.filter(Q(is_superuser=True) & Q(is_marketer=True) & Q(is_admin=False))
        
    }
    return render(request, 'aberd/superusersaccounts.html', context)



from django.views.decorators.csrf import csrf_exempt

@login_required
def vps_view_summary_control_panel(request):
    if request.method == 'POST':
        form = SuperUserVPSAccountForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.obj_type = 'vps'
            obj.save()
            
    context = {
        "vpses": OrderDetail.objects.filter(Q(instance__obj_type='vps')  & Q(instance__sold=True) ).order_by('id'),
        'vpsform': SuperUserVPSAccountForm,
    }
    return render(request, 'aberd/vpsviewsummary.html', context)

from .forms import ManualSuperUserVPSAccountForm

@login_required
def vps_manual_control_panel(request):    
    if request.method == 'POST':
        template = request.POST.get('template')
        hostname = request.POST.get('hostname')
        instance_id = request.POST.get('instance_id')
        account =   request.POST.get('aws_account')
        cloud =   request.POST.get('cloud')

        account = AwsAccounts.objects.get(id=account)


        template = Templates.objects.get(id=template)
        
        try:
            old_instance = VPS.objects.get(instance_id=instance_id)
            old_instance.instance_id = str(old_instance.instance_id) + ':manual'
            old_instance.save()
        except Exception as e:
            print(e)

        vps  = VPS(
            obj_type='vps',
            template=template,
            instance_id = instance_id,
            aws_account=account,
            hostname = hostname,
            cloud=cloud,
            date_created=datetime.datetime.now()
        )
        vps.save()
        

        
            
    context = {
        "vpses": VPS.objects.filter(Q(obj_type='vps')  & Q(sold=False) & Q(template__generation='manual')).order_by('id'),
        'vpsform': ManualSuperUserVPSAccountForm,
    }
    return render(request, 'aberd/vpsmanual.html', context)


@login_required()
def proxy_view_summary(request):
    # proxies = chain(
    #     VPS.objects.filter(Q(obj_type='proxy')  & Q(sold=True)).order_by('id'),
    # )
    # for p in VPS.objects.filter(Q(obj_type='proxy')  & Q(sold=True)).order_by('id'):
    #     print(p)
    context = {
        # "proxies": proxies,
        # "proxies": OrderDetail.objects.filter(Q(instance__obj_type='proxy')  & Q(instance__sold=True)).order_by('id'),
        "proxies": OrderDetail.objects.filter(Q(instance__obj_type='proxy')  &Q(instance__sold=True)).order_by('id'),
        'proxyform': SuperUserPROXYAccountForm,
    }
    return render(request, 'aberd/proxyviewsummary.html', context)

@login_required()
def manual_proxy(request):
    man_proxies = chain(
        VPS.objects.filter(Q(obj_type='proxy') & Q(template__generation='manual') & Q(deleted=False) & Q(sold=False)).order_by('id'),
    )
    context = {
        "man_proxies": man_proxies,
        'manual_proxyform': ManualSuperUserPROXYAccountForm,
    }
    return render(request, 'aberd/manualviewsummary.html', context)



@login_required()
def vpn_view_summary(request):
    context = {
        # "proxies": VPS.objects.filter(Q(obj_type='vpn')  & Q(sold=True)).order_by('id'),
        "proxies": OrderDetail.objects.filter(Q(instance__template__obj_type='vpn')  &Q(instance__sold=True)).order_by('id'),
        'proxyform': SuperUserPROXYAccountForm,
    }
    return render(request, 'aberd/vpnviewsummary.html', context)



from .forms import VPNFORM






import boto3
from .forms import CSVFIleForm
@login_required
def upload_vpn_csv(request):
    context = {}
    if request.method == "POST":
        if request.user.is_admin:
            print(request.POST)
            print(request.FILES)
            form = CSVFIleForm(request.POST, request.FILES)
            region = 'ap-south-1'
            if form.is_valid():
                data = form.save()
                session = boto3.Session(
                    aws_access_key_id="AKIAYJPNBQCGQX74CJJD",
                    aws_secret_access_key="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",
                    region_name=region
                )
                s3 = session.resource('s3')
                bucket = 'manual-vpn'

                file = request.FILES['csv_file']
                data = open(data.csv_file.path, 'r', encoding="utf-8")
                r = data.read()
                decoded_file = data.read()
                
                object = s3.Object(bucket, 'upload.csv')

                result = object.put(Body=r)
            
                print(result)
                messages.success(request, 'Upload Successful')
                return redirect(reverse('upload_vpn_csv'))
            messages.error(request, form.errors)
        return redirect(reverse('upload_vpn_csv'))
    
    context = {
        'files': CsvFile.objects.all(),
        'csvform': CSVFIleForm 
        }
    return render(request, 'aberd/upload_vpn_csv.html', context)
        
        
        




@login_required
def control_panel_vpn(request):
    if request.user.is_admin:
        if request.method == 'POST':
            aws_account_id = request.POST.get('aws_account_id')
            user_id = request.POST.get('user_id')
            template = request.POST.get('template')
            password =   request.POST.get('password')
            account =   request.POST.get('aws_account')
            account = AwsAccounts.objects.get(id=account)

            user = CustomUser.objects.filter(username=user_id)
            if user.count() > 0:
                user = user.first()
            else:
                user, new = CustomUser.objects.get_or_create(
                    username = user_id,
                    is_superuser=True,
                    is_active=True
                )
                user.set_password(password)
                user.save()
  
            #check for instances
            instances = VPS.objects.filter(Q(user=user) & Q(obj_type='proxy'))
            if instances.count() > 0:
                messages.error(request, 'This User Has A Proxy Associated Already')
                return redirect(reverse('control_panel'))
            vps  = VPS(
                obj_type='vpn',
                user=user,
                password=password,
                template=Templates.objects.get(id=template),
                aws_account=account,
                date_created=datetime.datetime.now()

            )
            vps.save()
        return redirect(reverse('control_panel'))
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect('/login')



@login_required()
def manual_vpn(request):
    form = VPNFORM()
    if request.method == 'POST':
        print(request.POST)
        form  = VPNFORM(request.POST, request.FILES)
        if form.is_valid():
            sa = form.save(commit=False)
            sa.obj_type='vpn'
            sa.save()
            return redirect(reverse('manual_vpn'))
        else:
            form = VPNFORM(request.POST, request.FILES),

            
    man_proxies = chain(
        VPS.objects.filter(Q(obj_type='vpn') & Q(sold=False)).order_by('id'),
    )
    context = {
        "man_proxies": man_proxies,
        'manual_proxyform': form,
    }
    return render(request, 'aberd/manualvpnviewsummary.html', context)

@login_required()
def edit_manual_vpn(request, pk):
    instance = VPS.objects.get(id=pk)
    form = VPNFORM()
    if request.method == 'POST':
        print(request.POST)
        form  = VPNFORM(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            sa = form.save(commit=False)
            sa.obj_type='vpn'
            sa.save()
            
            return redirect(reverse('manual_vpn'))
        else:
            form = VPNFORM(request.POST, request.FILES, instance=instance)
    man_proxies = chain(
        VPS.objects.filter(Q(obj_type='vpn') & Q(sold=False)).order_by('id'),
    )
    context = {
        "man_proxies": man_proxies,
        'manual_proxyform': VPNFORM(instance=instance),
    }
    return render(request, 'aberd/edit_manualvpnviewsummary.html', context)

from utils.route53 import update_route53
@login_required
def manual_vpn_add_control_panel_vpn(request):
    if request.method == 'POST':
        form  = VPNFORM(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect(reverse('manual_vpn_add_control_panel_vpn'))

@login_required
def edit_manual_vpn_add_control_panel_vpn(request, pk):
    vps, new = VPS.objects.get_or_create(id=pk)
    if request.method == 'POST':
        form  = VPNFORM(request.POST, request.FILES, instance=vps)
        if form.is_valid():
            form.save()
        return redirect(reverse('manual_vpn_add_control_panel_vpn'))
    context = {
        'manual_proxyform': VPNFORM(instance=vps)
    }
    return render(request, 'aberd/edit_manualvpnviewsummary.html', context)




















@login_required
def superuser_home(request):
    if request.user.is_superuser:
        account, new =  Accounts.objects.get_or_create(user=request.user)
        seller_ids = [p.user.id for p in VPS.objects.filter(super_seller=request.user)]
        proxies = len(VPS.objects.filter(Q(template__obj_type='proxy') & Q(created_by=request.user) & Q(deleted=False))) 
        vpses = len(VPS.objects.filter(Q(template__obj_type='vps') & Q(created_by=request.user) & Q(deleted=False)))
        vpnes = len(VPS.objects.filter(Q(template__obj_type='vpn') & Q(created_by=request.user) & Q(deleted=False)))
        # users = len(CustomUser.objects.filter(created_by=request.user))
        context = {
            'date': datetime.datetime.now(),
            'date3': datetime.datetime.now().replace(tzinfo=None),
            'vpsform': PROXYFORM,
            'proxyform': PROXYFORM,
            'proxies': proxies,
            'users': 0,
            'vpses': vpses,
            'vpnes': vpnes,
            'templates_auto': Templates.objects.filter(~Q(generation__in=['manual']) & Q(super_user__in=[request.user, ])),
            'templates': Templates.objects.filter(Q(generation='manual') & Q(super_user__in=[request.user, ])),
            'seller_templates_offers': SellerTemplates.objects.filter(Q(seller=request.user)),
            'account': account,
            'seller_form': SellerForm,
            'sellers': VPS.objects.filter(super_seller=request.user),
            'seller_templates': SellerTemplates.objects.filter(Q(created_by=request.user) | Q(seller=request.user)),
        }
        return render(request, 'aberd/superuser_home.html', context)
    messages.error(request, 'You don not have access to this page')
    return redirect(reverse("index"))




@login_required()
def create_instance__u(request):
    account, new =  Accounts.objects.get_or_create(user=request.user)

    context = {
        'account': account,
        'users': CustomUser.objects.filter(Q(is_superuser=True) & Q(deleted=False)).order_by('id'),
        'templates_auto': Templates.objects.filter(~Q(generation__in=['manual']) & Q(super_user__in=[request.user, ])),
        'templates': Templates.objects.filter(Q(generation='manual') & Q(super_user__in=[request.user, ])),
        'seller_templates_offers': SellerTemplates.objects.filter(Q(seller=request.user)),
        'seller_templates': SellerTemplates.objects.filter(Q(created_by=request.user) | Q(seller=request.user)),
    }
    return render(request, 'aberd/create_instance.html', context)

@login_required()
def vps_history_spu(request):

    context = {
        'orders': OrderDetail.objects.filter(Q(customer=request.user) & Q(package__template__obj_type='vps') & Q(has_paid=True))
    }
    return render(request, 'aberd/vps_history_spu.html', context)


from .forms import VPNFORM

@login_required()
def vpn_history_spu(request):

    context = {
        'orders': OrderDetail.objects.filter(Q(customer=request.user) & Q(package__template__obj_type='vpn') & Q(has_paid=True))


    }
    return render(request, 'aberd/vpn_history_spu.html', context)



@login_required()
def proxies_history_spu(request):

    context = {
        'orders': OrderDetail.objects.filter(Q(customer=request.user) & Q(package__template__obj_type='proxy') & Q(has_paid=True))
    }
    return render(request, 'aberd/proxies_history_spu.html', context)








@login_required
def superuser_add_vpn(request):
    if request.user.is_admin:
        if request.method == 'POST':
            aws_account_id = request.POST.get('aws_account_id')
            user_id = request.POST.get('user_id')
            password =   request.POST.get('password')

            user, new = CustomUser.objects.get_or_create(
                username = user_id,
                is_active=True
            )
            user.set_password(password)
            user.save()
            vps  = VPS(
                sub_type='vpn',
                user=user,
                days=0,
                hours=0,
                usage=0,
                password=password,
                aws_account_id=aws_account_id,
                created_by=request.user,
                date_created=datetime.datetime.now()


            )
            vps.save()
        return redirect(reverse('superuser_dashboard'))
    logout(request)
    messages.success(request, 'You do  not have permission. Session Closed') 
    return redirect('/login')































from utils.ssh import update_instance_through_ssh
@login_required
def GEN_REA(request, pk):


    number_of_instances = 1

    template = Templates.objects.get(id=pk)
    
    print(template.cost.amount)
    print("))))))))))))))))))))))))))))")

    if template.generation == 'auto':
        account, new = Accounts.objects.get_or_create(
            user=request.user,
        )
        if Decimal(account.balance.amount) >= (Decimal(template.cost.amount) * Decimal(int(number_of_instances))):
            client = get_client(template, request.user, VPS)

            if template.obj_type == 'vps':

                try:
                    response = create_instance(client, template.template_id, number_of_instances, number_of_instances)
                    print(response)
                    for instance in response["Instances"]:
                        instance = instance
                        waiter = client.get_waiter('instance_running')
                        res = waiter.wait(InstanceIds=[instance['InstanceId']])
                        vps = VPS(
                            instance_id= instance['InstanceId'],
                            aws_account=template.aws_account,
                            obj_type = 'vps',
                            state= instance['State']['Name'],
                            created_by=request.user,
                            template=template,
                            date_created=datetime.datetime.now()
                        )
                        vps.save()
                        
                        hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()
                        print(hostname)
                        vps.hostname = hostname
                        vps.port = template.port
                        vps.instance_user = template.user
                        vps.instance_password = template.password
                        vps.summary = summary
                        vps.save()
                        account.balance = Decimal(account.balance.amount) - Decimal(template.cost.amount)
                        account.save()
                        log = AccountLogs.objects.create(
                            description="Generated",
                            account=account,
                            amount=Decimal(template.cost.amount) * -1,
                            balance=account.balance,
                            instance=vps,

                        )
                        log.save()
                        usage = Usage(
                            instance=vps,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        vps.current_usage = usage
                        vps.save()

                        print('Updating SSH')

                except Exception as e:
                    print(e)
                    messages.error(request, f'Something went wrong Please Contact The Administrator')
            elif template.obj_type == 'proxy':

                try:
                    response = create_instance(client, template.template_id, number_of_instances, number_of_instances)
                    print(response)
                    print("Connecting and trying")
                    for instance in response['Instances']:
                        print(instance)
                        waiter = client.get_waiter('instance_running')
                        res = waiter.wait(InstanceIds=[instance['InstanceId']])
                        vps = VPS(
                            instance_id= instance['InstanceId'],
                            aws_account=template.aws_account,
                            obj_type = 'proxy',
                            state= instance['State']['Name'],
                            created_by=request.user,
                            template=template,
                            date_created=datetime.datetime.now()
                        )
                        vps.save()
                        print('Created Instance')
                        hostname, port, date, time, password, keyname, summary, user = vps.update_hostname()
                        print(hostname)
                        vps.hostname = hostname
                        vps.port = template.port
                        vps.instance_user = template.user
                        vps.instance_password = template.password
                        vps.summary = summary
                        vps.save()
                        account.balance = Decimal(account.balance.amount) - Decimal(template.cost.amount)
                        account.save()
                        log = AccountLogs.objects.create(
                            description="Generated",
                            account=account,
                            amount=Decimal(template.cost.amount) * -1,
                            balance=account.balance,
                            instance=vps
                        )
                        log.save()
                        usage = Usage(
                            instance=vps,
                            start_date = datetime.datetime.now()
                        )
                        usage.save()
                        vps.current_usage = usage
                        vps.save()

                        messages.success(request, f'Successfully created')

                except Exception as e:
                    print(e)

                    messages.error(request, f'Something went wrong Please Contact The Administrator')
        
        else:
            messages.error(request, f"Your Account does have enough balance to generate the {number_of_instances} instance")
    


