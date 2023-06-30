# Generated by Django 3.2.6 on 2022-09-28 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0076_vps_instance_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvfile',
            name='csv_file',
            field=models.FileField(blank=True, default='D:\\work\\tom\\tom_aberd\\rdprdp_file.rdp', max_length=254, null=True, upload_to='csv/'),
        ),
        migrations.AlterField(
            model_name='rdpfile',
            name='rdp_file',
            field=models.FileField(blank=True, default='D:\\work\\tom\\tom_aberd\\rdprdp_file.rdp', max_length=254, null=True, upload_to='rdp/'),
        ),
        migrations.AlterField(
            model_name='vps',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]