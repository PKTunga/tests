# Generated by Django 3.2.6 on 2021-09-01 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_alter_awsaccounts_ssh_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awsaccounts',
            name='ssh_key',
            field=models.FileField(blank=True, max_length=254, null=True, upload_to='media/'),
        ),
    ]
