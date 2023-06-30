# Generated by Django 3.2.6 on 2021-09-05 20:30

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_paymentpic_rdpfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentpic',
            name='banner_file',
            field=stdimage.models.StdImageField(blank=True, default='user.jpg', null=True, upload_to='media/', verbose_name='Payment Banner'),
        ),
        migrations.AlterField(
            model_name='rdpfile',
            name='rdp_file',
            field=stdimage.models.StdImageField(blank=True, default='user.jpg', null=True, upload_to='media/', verbose_name='RDP File'),
        ),
    ]
