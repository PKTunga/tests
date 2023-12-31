# Generated by Django 3.2.6 on 2021-09-05 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_auto_20210902_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_file', models.FileField(blank=True, default='D:\\work\\tom\\New folder\\rdp\\rdp_file.rdp', max_length=254, null=True, upload_to='media/')),
            ],
        ),
        migrations.CreateModel(
            name='RDPFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rdp_file', models.FileField(blank=True, default='D:\\work\\tom\\New folder\\rdprdp_file.rdp', max_length=254, null=True, upload_to='media/')),
            ],
        ),
    ]
