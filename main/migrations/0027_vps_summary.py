# Generated by Django 3.2.6 on 2021-08-21 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20210821_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='summary',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
