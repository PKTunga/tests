# Generated by Django 3.2.6 on 2022-12-20 10:39

import authenticate.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0017_whatsappnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referral_token',
            field=models.CharField(default=authenticate.models._default_token, max_length=255),
        ),
    ]
