# Generated by Django 3.2.6 on 2021-08-25 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20210825_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='key_name',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='ssh_key',
        ),
        migrations.AddField(
            model_name='awsaccounts',
            name='key_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='awsaccounts',
            name='ssh_key',
            field=models.FileField(blank=True, default='settings.RDP_FOLDER/rdp_file.rdp', max_length=254, null=True, upload_to='ssh_keys/'),
        ),
    ]