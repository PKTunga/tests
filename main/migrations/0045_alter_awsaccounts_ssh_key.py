# Generated by Django 3.2.6 on 2021-09-01 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_rename_pssword_awsaccounts_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awsaccounts',
            name='ssh_key',
            field=models.FileField(blank=True, max_length=254, null=True, upload_to='media/'),
        ),
    ]
