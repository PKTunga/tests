# Generated by Django 3.2.6 on 2022-12-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralrelationship',
            name='date_created',
            field=models.DateField(auto_now=True, null=True, verbose_name='Date created'),
        ),
    ]