# Generated by Django 3.2.6 on 2022-09-01 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0069_auto_20220823_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='vpn_file',
            field=models.FileField(blank=True, default='', max_length=254, null=True, upload_to='vpn_file/'),
        ),
        migrations.AddField(
            model_name='vps',
            name='vpn_key',
            field=models.FileField(blank=True, default='', max_length=254, null=True, upload_to='vpn_key/'),
        ),
    ]