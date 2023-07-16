from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group 
from django.utils import timezone
from django.utils.http import urlquote
from django.shortcuts import reverse
from django.conf import settings

from main.models import Accounts, SellerTemplates
from django.contrib.auth.models import BaseUserManager
from decimal import Decimal

          
from allauth.account.models import EmailAddress


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given email must be set')
        user = self.model(username=username,
                          is_admin=True,
                          is_staff=is_staff, is_active=True,
                          is_superuser=True, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)



from main.models import VPS, Accounts
from itertools import chain


from django.core.validators import RegexValidator
from referrals.models import ReferralRelationship
import uuid
def _default_token():
    return uuid.uuid4().hex 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    Male = 'M'
    Female = 'F'
    genders = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    alias = models.CharField(max_length=12, help_text='Username is Required', null=True)
    email = models.EmailField(_('Email Address'), null=True)
    username = models.CharField(max_length=20, help_text='Username is Required',  null=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, default="", blank=True, null=True)
    middle_name = models.CharField(_('Middle name'), max_length=30, default="", blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, default="", blank=True, null=True)
    gender = models.CharField(choices=genders, max_length=12, default='F', null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=_("User Role"), on_delete=models.CASCADE)
    is_admin = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    deleted = models.BooleanField(_('deleted'), default=False,
        help_text=_('Delete.'))
    is_seller = models.BooleanField(_('Is seller'), default=False,
        help_text=_('User is a seller'))
    is_marketer = models.BooleanField(_('Is Marketer'), default=False,
        help_text=_('User is a Marketer'))
    seller_quantity = models.IntegerField(default=0)
    seller_credit = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    seller_template = models.ForeignKey('main.SellerTemplates', null=True, blank=True, on_delete=models.DO_NOTHING)
    is_normal = models.BooleanField(_('Is Normal'), default=False,
        help_text=_('User is a Normal User'))
    referral_token = models.CharField(max_length=255, default=_default_token)
    my_inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='My inviter+',
        verbose_name="My inviter",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["referral_token", "email"]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    
    @property
    def get_referral_link(self):
        return reverse('generate_referrals', args=(self.username,))
    # request.build_absolute_uri(reverse('generate_referrals', args=(self.username, )))
    
    
    @property
    def get_referrer(self):
        referrer = ReferralRelationship.objects.filter(invited=self)
        if referrer.count() > 0:
            return referrer[0]
        else:
            return None
    

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def __str__(self):
        return "%s" % (self.username)
    
    @property
    def templates(self):
        ids = SellerTemplates.objects.filter(sellers__id__in=[self.id])
        ids_ = SellerTemplates.objects.filter(seller__id=self.id)
        result_list = list(chain(ids, ids_))
        return result_list

    @property
    def balance(self):
        account, new = Accounts.objects.get_or_create(user=self)
        return account.balance

    @property
    def get_aws_account(self):
        # vps = VPS.objects.filter(user=self)
        # if vps.count() > 0:
        #     return vps.first().aws_account.account_id
        # else:
        return None
        
        
    @property
    def get_seller_credit(self):
        return Decimal(0.00)
    
    @property
    def verified(self):
        e = EmailAddress.objects.get(user=self)
        return e.verified

    @property
    def get_password(self):
        vps = VPS.objects.filter(user=self)

        if self.is_superuser:
            if self.first_name != None:
                return self.first_name

        if vps.count() == 0:
            return self.first_name
        
        if vps.count() > 0:
            return vps.first().password
        else:
            return None
        
        
    def set_password_vps(self, password):
        vps = VPS.objects.filter(user=self)
        if len(vps) > 0:
            vps= vps.first()
            vps.password = password
            vps.save()
        return None


class LoginMessage(models.Model):
    message = models.CharField(_('Super User Accounts Login Message'), max_length=250, blank=True, null=True)
    basic = models.CharField(_('User Accounts Login Message'), max_length=250, blank=True, null=True)

class BannerMessage(models.Model):
    header = models.TextField(_('Header'), max_length=1000, blank=True, null=True)
    subtext = models.TextField(_('sub text'), max_length=1000, blank=True, null=True)

from django.conf import settings

User = settings.AUTH_USER_MODEL
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.id
    
    
    
class WhatsappNumber(models.Model):
    number = models.CharField(_('Whatsapp Phone Number '), max_length=50, blank=True, null=True)
    link = models.CharField(_('Telegram Link'), max_length=150, blank=True, null=True, default="")


class DailyNews(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=500, default="Welcome to Proxy World")  # Set a maximum length of 500 characters
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Video(models.Model):
    title = models.CharField(max_length=100)
    video_id = models.CharField(max_length=30)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
