# Generated by Django 3.2.6 on 2021-08-20 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_accountlogs_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='date_generated',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='vps',
            name='hostname',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vps',
            name='instance_password',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vps',
            name='instance_user',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vps',
            name='port',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vps',
            name='time_generated',
            field=models.TimeField(null=True),
        ),
    ]