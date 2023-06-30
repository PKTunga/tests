from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.ec2 import *
from django.conf import settings
from django.db.models import Sum, Aggregate
from decimal import Decimal
from djmoney.models.fields import MoneyField
from django.db import models


import datetime
types = (
    ('vps', 'VPS'),
    ('proxy', 'PROXY'),
    ('vpn', 'VPN'),
)
clouds_ = (
    ('aws', 'AWS'),
    ('goldproxyvps', 'Gold Proxy Vps'),
)
class VPS(models.Model):
    obj_type = models.CharField(max_length=20, choices=types)
    sub_type = models.CharField(max_length=20, choices=types, default='vps')
    aws_account = models.ForeignKey('main.AwsAccounts', default=None, on_delete=models.DO_NOTHING, null=True, blank=True)
    instance_id = models.CharField(max_length=50,  null=True)
    state = models.CharField(max_length=50,  null=True)
    vps_name = models.CharField(max_length=50, null=True, default='', blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    hours = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    usage = models.IntegerField(default=0)
    date_generated = models.DateField(auto_now=False, null=True)
    time_generated = models.TimeField(null=True)
    current_usage = models.ForeignKey('main.Usage', related_name='Usage+', on_delete=models.CASCADE, null=True, blank=True)
    summary = models.CharField(max_length=50,  null=True, blank=True)
    hostname = models.CharField(max_length=50,  null=True, blank=True)
    port = models.CharField(max_length=50,  null=True, blank=True)
    instance_user = models.CharField(max_length=50, verbose_name=_("Username"), null=True, blank=True)
    instance_password = models.CharField(max_length=50,  verbose_name=_("Password"), null=True, blank=True)
    instance_email = models.EmailField(null=True, blank=True)

    template = models.ForeignKey('main.Templates', related_name='Templates+', on_delete=models.SET_NULL, null=True, blank=True)
    rdp_file = models.FileField(upload_to='rdp_files/', max_length=254, null=True, blank=True, default='settings.RDP_FOLDER/rdp_file.rdp')
    ssh_key = models.FileField(upload_to='ssh_keys/', max_length=254, null=True, blank=True, default='settings.RDP_FOLDER/rdp_file.rdp')
    key_name = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey('authenticate.CustomUser', related_name='Custom User+', on_delete=models.CASCADE, null=True, blank=True)
    balance =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')
    user_attached = models.BooleanField(default=False)
    proxy_details_set = models.BooleanField(default=False)
    proxy_details = models.CharField(max_length=50, default="")
    date_created = models.DateField(_("Date created"), auto_now=False,  null=True, blank=False)
    created_by = models.ForeignKey("authenticate.CustomUser", null=True, blank=True, related_name="Creator+", verbose_name=_("Created by"), on_delete=models.CASCADE)
    date_modified = models.DateField(_("Date Modified"),null=True, blank=True, auto_now=True)
    modified_by = models.ForeignKey("authenticate.CustomUser",  null=True, blank=True, related_name="Modifier+", verbose_name=_("Modified by"), on_delete=models.CASCADE)
    deleted = models.BooleanField(_('deleted'), default=False,
        help_text=_('Delete.'))
    assigned = models.BooleanField(default=False)
    super_seller = models.ForeignKey("authenticate.CustomUser", null=True, blank=True, verbose_name=_("Super Seller"), on_delete=models.CASCADE)
    vpn_file = models.FileField(upload_to='vpn_file/', verbose_name=_("Vpn Client"), max_length=254, null=True, blank=True, default='')
    vpn_key = models.FileField(upload_to='vpn_key/', verbose_name=_("Vpn Profile"), max_length=254, null=True, blank=True, default='')
    sold = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    cloud = models.CharField(max_length=20, choices=clouds_, default='aws')

    # def __str__(self):
    #     return str(self.id)

    @property
    def get_credit(self):
        try:
            account, new = Accounts.objects.get_or_create(
                user=self.user
            )
            return account.balance

        except AttributeError as e:
            return False

    @property
    def usage_(self):
        return self.days * self.hours


    def target_date(self):
        from payments.models import order_date_function
        order_date = order_date_function(self)
        if order_date != None:
          date_1 = order_date
          if date_1 == None:
              date_1 = datetime.datetime.now().date()
        else:
          date_1 = self.date_created
          if date_1 == None:
              date_1 = datetime.datetime.now().date()
        end_date = date_1 + datetime.timedelta(days=30)
        return end_date
    
    # def target_date(self):
    #     date_1 = self.date_created
    #     end_date = date_1 + datetime.timedelta(days=30)
    #     return end_date


    def days_not_active(self):
        try:
          days_in_use = self.target_date().date() - datetime.datetime.now().date()
        except Exception as e:
          days_in_use = self.target_date() - datetime.datetime.now().date()
        return days_in_use.days

    @property
    def usage_in_hours(self):
        usage = Usage.objects.filter(instance=self)
        total = int(0.0)
        for usage in usage:
            total += int(usage.usage)
        return total


    @property
    def get_date(self):
        if self.date_modified is not None:
            return self.date_modified
        return self.date_created
    


    @property
    def usage_in_days(self):
        return self.days_not_active()



    def describe_instance(self, client):

        try:
            response = client.describe_instances(
                InstanceIds=[
                    self.instance_id
                ],
            )
            try:
                try:
                    status = response['Reservations'][0]
                    print(status)
                    return status
                except IndexError as e:
                    return 'Un-Known'
            except KeyError as e:
                return 'Un-Known'
        except ClientError as e:
            return 'Un-Known'

    # def status(self, client):
    #     try:
    #         response = client.describe_instances(
    #             InstanceIds=[
    #                 self.instance_id
    #             ],
    #         )
    #         try:
    #             try:
    #                 status = response['Reservations'][0]['Instances'][0]['State']['Name']
    #                 return status
    #             except IndexError as e:
    #                 return 'Un-Known'
    #         except KeyError as e:
    #             return 'Un-Known'
    #     except ClientError as e:
    #         return 'Un-Known'
        
    def status(self, client):
        if self.cloud == 'aws':
            try:
                response = client.describe_instances(
                    InstanceIds=[
                        self.instance_id
                    ],
                )
                try:
                    try:
                        status = response['Reservations'][0]['Instances'][0]['State']['Name']
                        return status
                    except IndexError as e:
                        return 'Un-Known'
                except KeyError as e:
                    return 'Un-Known'
            except ClientError as e:
                return 'Un-Known'
        else:
            return 'running'

    def stop(self, client):
        try:
            response = client.stop_instances(
                InstanceIds=[
                    self.instance_id
                ],
            )
            return
        except ClientError as e:
            return 'Failed'

    def start(self, client):
        try:
            response = client.start_instances(
                InstanceIds=[
                    self.instance_id
                ],
            )
            return "Instance Running"
        except ClientError as e:
            return 'Failed'

    def public_ip(self, client):
        try:
            response = client.start_instances(
                InstanceIds=[
                    self.instance_id
                ],
            )
            return response['Reservations'][0]['Instances'][0]['State']
        except ClientError as e:
            return 'Failed'

    def terminate(self, client):
        try:
            response = client.terminate_instances(
                InstanceIds=[
                    self.instance_id
                ],
            )

            return "Instance Stoppe"
        except ClientError as e:
            return 'Failed'

    @property
    def current_usage_(self):
        if self.current_usage != None:
            return self.current_usage.usage
        return 0

 

    def update_hostname(self):
        session = boto3.Session(
            aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
            region_name='ap-south-1'
        )
        dynamo_client = session.resource('dynamodb')
        table_name = dynamo_client.Table('DnsAutoNamerTable')
        key_ = self.instance_id +"+"+ self.aws_account.account_id
        print("TTTTTTTTTTTTTTTTTTTTT")
        print("TTTTTTTTTTTTTTTTTTTTT")
        print("TTTTTTTTTTTTTTTTTTTTT")
        print("TTTTTTTTTTTTTTTTTTTTT")
        print(key_)
        response = table_name.query(
            KeyConditionExpression=Key('keyname').eq(key_)
        )
        print(response)
        hostname = ''
        port = ''
        date = ''
        time = ''
        password = ''
        keyname = ''
        summary = ''
        user = ''
        try:
            instance = response['Items'][0]
            print(instance)
            try:
                date = instance['date']
            except KeyError as e:
                date = ''
            try:
                time = instance['time']
            except KeyError as e:
                time = ''
            try:
                hostname = instance['hostname']
            except KeyError as e:
                hostname = ''

            try:
                port = instance['port']
            except KeyError as e:
                port = ''
            try:
                user = instance['user']
            except KeyError as e:
                user = ''
            try:
                password = instance['password']
            except KeyError as e:
                password = ''

            try:
                summary = instance['summary']
            except KeyError as e:
                summary = ''

            return hostname, port, date, time, password, keyname, summary, user
        except IndexError as e:
            print("ERRRRRRRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRr")
            print(e)

            return hostname, port, date, time, password, keyname, summary, user

    @property
    def get_summary(self):
        if self.template != None:
 
            if self.template.generation == 'manual':
                if self.template.port == '' and self.template.user == '' and self.template.password == '':
                    return f'{self.summary}'
                if self.template.port == None and self.template.user == None and self.template.password == None:
                    return f'{self.summary}'
                return f'{self.summary}:{self.template.port}:{self.template.user}:{self.template.password}'
        if self.port != '' and self.instance_user != '' and self.instance_password != '':
            return f'{self.hostname}:{self.port}:{self.instance_user}:{self.instance_password}'
        else:
            return f'{self.hostname}:{self.template.port}:{self.template.user}:{self.template.password}'



    def generate_rdp(self):
        import os 
        from shutil import copyfile
        src = settings.RDP_FILE
        file_name =  f"{self.user.username}.rdp"
        f = open(os.path.join(settings.MEDIA_ROOT, file_name), "a")
        f.close()
        file_ = os.path.join(settings.MEDIA_ROOT, file_name)
        copyfile(src, file_)
        my_file = open(file_)
        string_list = my_file.readlines()
        string_list[0] = string_list[1] + " Twende Nami\n"
        string_list[2] = "full address:s:visor\n"
        string_list[3] = "username:s:Kamau\n"
        my_file = open(file_, "w")
        new_file_contents = "".join(string_list).encode('UTF-8')
        my_file.write(new_file_contents)
        my_file.close()
        self.rdp_file = file_
        self.save()
        return 
gen_ = (
    ('auto', 'AUTO'),
    ('manual', 'MANUAL'),
)
class Templates(models.Model):
    template_name = models.CharField(max_length=20)
    template_id = models.CharField(max_length=20)
    obj_type = models.CharField(max_length=20, choices=types, default='vps')
    generation = models.CharField(max_length=20, choices=gen_, default='auto')
    user = models.CharField(max_length=50,  null=True)
    port = models.CharField(max_length=50,  null=True)
    password = models.CharField(max_length=50,  null=True)
    # cost = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    cost =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')
    # total_cost = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    total_cost =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')
    # super_user = models.ForeignKey("authenticate.CustomUser", null=True, blank=True, related_name="Super User+", verbose_name=_("Super User"), on_delete=models.CASCADE)
    super_user = models.ManyToManyField("authenticate.CustomUser", related_name="Super User+", verbose_name=_("Super User"), null=True, blank=True)
    aws_account = models.ForeignKey('main.AwsAccounts', on_delete=models.SET_NULL, null=True, blank=False)
    date_created = models.DateField(_("Date created"), auto_now_add=True)
    create_by = models.ForeignKey("authenticate.CustomUser", null=True, blank=True, related_name="Creator+", verbose_name=_("Created by"), on_delete=models.CASCADE)
    date_modified = models.DateField(_("Date Modified"),null=True, blank=True, auto_now=False)
    modified_by = models.ForeignKey("authenticate.CustomUser",  null=True, blank=True, related_name="Modifier+", verbose_name=_("Modified by"), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.generation} - {self.template_name}'



class SellerTemplates(models.Model):
    # def __init__(self, *args, **kwargs):
    #     super(SellerTemplates, self).__init__(*args, **kwargs)
    #     self._old_cost = self.cost
    #     self._old_quantity = self.quantity

    template = models.ForeignKey("main.Templates", related_name="Templates+", verbose_name=_("Templates"), on_delete=models.CASCADE, null=True, blank=True)
    sellers = models.ManyToManyField("authenticate.CustomUser", verbose_name=_("Avail To Sellers"),)
    seller = models.ForeignKey("authenticate.CustomUser",related_name="seller+", verbose_name=_("Avail To Sellers"),null=True, blank=True, on_delete=models.CASCADE)
    # cost = models.DecimalField(default=0.00, max_digits=15, decimal_places=2,verbose_name=_("Cost Per Item"))
    cost =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD',verbose_name=_("Cost Per Item"))
    # total_cost =  models.DecimalField(default=0.00, max_digits=15, decimal_places=2,verbose_name=_("Total Cost"))
    total_cost =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD',verbose_name=_("Total Cost"))
    quantity = models.IntegerField(default=0, verbose_name=_("Quantity"))
    date_created = models.DateField(_("Date created"), auto_now_add=True)
    created_by = models.ForeignKey("authenticate.CustomUser", null=True, blank=True, related_name="Creator+", verbose_name=_("Created by"), on_delete=models.CASCADE)
    date_modified = models.DateField(_("Date Modified"),null=True, blank=True, auto_now=False)
    modified_by = models.ForeignKey("authenticate.CustomUser",  null=True, blank=True, related_name="Modifier+", verbose_name=_("Modified by"), on_delete=models.CASCADE)
    
    
    # def __str__(self):
    #     return f"{self.template.template_name} {self.total_cost}"
    
    
    @property
    def get_seller_name(self):
        return f"{self.template.template_name} {self.cost}"


    @property
    def total_price(self):
        if self.template.total_cost == 0:
            return self.cost * self.quantity
        return self.template.total_cost
    
    
    @property
    def get_total_cost(self):
        # if self.template.total_cost == 0:
        return self.template.cost * self.quantity
        # return self.template.total_cost
        
    @property
    def get_total_price(self):
        # if self.template.total_cost == 0:
        if self.seller != None:
            account =  Accounts.objects.filter(user=self.seller).first()
            return account.balance
        return self.cost * self.quantity
    
    # def save(self, *args, **kwargs):
    #     if self._old_cost  != self.cost or self._old_quantity != self.quantity:
    #         old = self._old_cost * self._old_quantity
    #         new = self.cost * self.quantity
    #         self.total_cost = self.total_cost - old
    #         self.total_cost = self.total_cost + new
    #         self.save()
            
    #     if self._old_quantity != self.quantity:
    #         template = self.template
    #         old = template.cost * self._old_quantity
    #         new = template.cost * self.quantity
    #         template.total_cost = template.total_cost - old
    #         template.total_cost = template.total_cost + new
    #         template.save()
            
    #     super(SellerTemplates, self).save(*args, **kwargs)



class AwsAccounts(models.Model):
    account_id = models.CharField(max_length=50)
    access =  models.CharField(max_length=50)
    secret =  models.CharField(max_length=50)
    username = models.CharField(max_length=50, default="centos")
    password = models.CharField(max_length=50, default="centos")
    ssh_key = models.FileField(upload_to='ssh_keys/', max_length=254, null=True, blank=True)
    key_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.account_id

    def create_ssh_key(self, client, access, secret):
        keypair_name = f'awsproxykey.pem'
        try:
            try:
                response = client.create_key_pair(KeyName=keypair_name)
                print(response)
                try:
                    private_key_file=open(os.path.join(settings.RDP_FOLDER, keypair_name),"w")
                    private_key_file.write(response['KeyMaterial'])
                    private_key_file.close

                    # self.
                    return keypair_name
                except ClientError as e:
                    print(e)
                    return False
            except ValueError as e:
                return False
        except ValueError as e:
            return False



    def __str__(self):
        return self.account_id



class Accounts(models.Model):
    user = models.ForeignKey('authenticate.CustomUser', related_name='Custom User+', on_delete=models.SET_NULL, null=True, blank=True)
    # balance = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    balance =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')

    # def __str__(self):
    #     return str(self.user.id)






from stdimage import StdImageField


import os
class PaymentPic(models.Model):
    banner_file = StdImageField(_("Payment Banner"), upload_to='payment/',
                          variations={'thumbnail': {'width': 100, 'height': 75}}, null=True, blank=True, default='payment.jpg')


class RDPFile(models.Model):
    rdp_file = models.FileField(upload_to='rdp/', max_length=254, null=True, blank=True, default=os.path.join(settings.RDP_FOLDER + "rdp_file.rdp"))


class CsvFile(models.Model):
    description = models.CharField(max_length=50, blank=True, null=True)
    csv_file = models.FileField(upload_to='csv/', max_length=254, null=True, blank=True, default=os.path.join(settings.RDP_FOLDER + "rdp_file.rdp"))















class AccountLogs(models.Model):
    description = models.CharField(max_length=50, blank=True, null=True)
    account = models.ForeignKey('main.Accounts', related_name='Account User+', on_delete=models.CASCADE, null=True, blank=True)
    # balance = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    balance =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')
    # amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    amount =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')
    date = models.DateTimeField(_("Date Modified"),null=True, blank=True, auto_now_add=True)
    instance = models.ForeignKey('main.VPS', related_name='VPS+', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey("authenticate.CustomUser", null=True, blank=True, related_name="Creator+", verbose_name=_("Created by"), on_delete=models.CASCADE)




    def __str__(self):
        return self.account_id

import pytz
class Usage(models.Model):
    start_date = models.DateTimeField(_("Start Modified"),null=True, blank=True, auto_now=False)
    stop_date = models.DateTimeField(_("Stop Modified"),null=True, blank=True, auto_now=False)
    instance = models.ForeignKey('main.VPS', related_name='VPS+', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=50, blank=True, null=True)


    @property
    def usage(self):
        import datetime
        utz=pytz.UTC
        date = datetime.datetime.now()
        # d = datetime.datetime.now()
        if self.stop_date != None:
            date = self.stop_date
        # tz = pytz.timezone('Asia/Kolkata')
        difference = self.start_date.replace(tzinfo=None) - date.replace(tzinfo=None)
        seconds_in_day = 24 * 60 * 60
        total = Decimal(divmod(difference.days * seconds_in_day + difference.seconds, 3600)[0])
        if total < 0:
            return total * -1
        return total 
# launchTime = utc.localize(launchTime) 

