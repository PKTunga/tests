# Generated by Django 3.2.6 on 2022-10-03 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0078_auto_20220928_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='csvfile',
            name='csv_file',
            field=models.FileField(blank=True, default='/home/tiger/awsvps/src/rdprdp_file.rdp', max_length=254, null=True, upload_to='csv/'),
        ),
        migrations.AlterField(
            model_name='rdpfile',
            name='rdp_file',
            field=models.FileField(blank=True, default='/home/tiger/awsvps/src/rdprdp_file.rdp', max_length=254, null=True, upload_to='rdp/'),
        ),
        migrations.AlterField(
            model_name='vps',
            name='vps_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
