"""
Django settings for aws_p project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'authenticate.CustomUser'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_2fn5g8c+aco0kv$)x5*4!g-wpe*9tnr3t8g*#o0=qp=46e1-%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [ 'www.goldvpsproxy.in','167.235.154.97', 'goldvpsproxy.in', '127.0.0.1', 'localhost', '78.47.56.34', 'proxyworld.in', 'www.proxyworld.in']

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'authenticate',
    
    'main',
    'crispy_forms',
    'django_crontab',
    'payments',
    'comply',
    'packages',
    'referrals',
    'djmoney',
    'djmoney.contrib.exchange',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'utils.auth_middleware.OneSessionPerUserMiddleware',
    'utils.middleware.parameters.ParametersMiddleware'

]

ROOT_URLCONF = 'setup.urls'
import os
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                
                
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]



SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },

}



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db9e2.sqlite3',
   },

    # 'default': {
    #       'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #       'NAME': 'tigerdb',
    #       'USER': 'tiger',
    #       'PASSWORD': 'tiger@#123#',
    #       'HOST': '127.0.0.1',
    #       'PORT': '5432',
    #   }

}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]



STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticroot")

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ACCOUNT_ADAPTER = 'authenticate.adapter.AccountAdapter'
ADMIN_LOGIN_REDIRECT_URL = '/control_panel'
SU_LOGIN_REDIRECT_URL = '/user_home'


LOGIN_REDIRECT_URL = '/'
SIGNUP_REDIRECT_URL = '/profile'
LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'


ACCOUNT_FORMS = {'signup': 'authenticate.forms.SignUpForm'}


env = environ.Env()
environ.Env.read_env()


AWS_SERVER_PUBLIC_KEY = 'AKIAYJPNBQCG6RDWDGWO'
AWS_SERVER_SECRET_KEY = '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'


RDP_FOLDER = os.path.join(BASE_DIR, 'rdp')
RDP_FILE = os.path.join(RDP_FOLDER, 'rdp_file.rdp')

# CELERY_TIMEZONE = "Australia/Tasmania"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60

# # CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
# # CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

# CELERY_BROKER_URL = "redis://localhost:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

CRONJOBS = [
    ('*\5 * * * *', 'main.tasks.check_for_instances_and_stop_them')
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'proxykeyworld@gmail.com'
EMAIL_HOST_PASSWORD = 'pernztrhsmyiqovc'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'proxykeyworld@gmail.com'

PAYTM_MERCHANT_ID = 'rUYIOW19577396738636'
PAYTM_SECRET_KEY = 'NxZfLdne@D_0sRc7'
PAYTM_WEBSITE = 'WEBSTAGING'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'

STRIPE_WEBHOOK_SECRET = ""

# CASHFREE_APPID = "200241e1c6176c3354fdda2b3b142002"
# CASHFREE_SECRET_KEY = "TESTaa45c03b6c9716aaafd6f6db6c5d960749229e96"
# CURRENCIES = ('INR')
CASHFREE_APPID = "2486760c0c523371555af3f992676842"
CASHFREE_SECRET_KEY = "b633febfee6e63c4a9c762f3e7b7e49ed1bac3d4"
DEAFULT_CURRENCY = 'INR'
DEAFULT_CURRENCY = 'INR'


# STRIPE_PUBLISHABLE_KEY = 'pk_live_51LdGGjSJR1UkEoD8p6ZeIl0XQRON4TpNpGh7r7VwwmSUT4H4F3okTqqGSSxOYaCwyXagqpAcAZai7jy2R7MjW1M500cotyIZT3'
# STRIPE_SECRET_KEY = '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'



# changed to new ones
# CASHFREE_APPID = "289783f0161e04b9f3f29b1cb4387982"
# CASHFREE_SECRET_KEY = "a2c189bc960301285c239aaa1a18b8febd0f4f2b"


STRIPE_SECRET_KEY = 'sk_test_51Ky6FFFQh9HqVz8CNqfI0qp9uWg89GuHNijuPzLXTaewJSpFt0SQ0wJpjJWNaC2ZgH8Yxd5U2U2HoeXAEpkgxGqM00wQLcAVmh'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51Ky6FFFQh9HqVz8CvF4BhPbeTPa7zu1lAGq8VYnTJKT8Qgfj0L3i0oZIXiGC3UkmMBsKaWNiIQ6hankEkDIY7zCO003tFyTGi2'



ACCOUNT_AUTHENTICATION_METHOD = 'username' 
ACCOUNT_USERNAME_REQUIRED = False
SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True 

# phonenumber
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "US"


#location
GOOGLE_API_KEY = ""

#recaptcha 
RECAPTCHA_PUBLIC_KEY = '6LcvE0MgAAAAAOBIrGEzc-GUkYnwYZXOWvY38QXg'
RECAPTCHA_PRIVATE_KEY = '6LcvE0MgAAAAAMT6kHj0lQGrLCa0hjcb2T2xGDRk'

RECAPTCHA_REQUIRED_SCORE = 0.95


# ATBBEPcmSNGQjD3xvfXEF7sD9r9vFCB33E01

