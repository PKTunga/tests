# Generated by Django 3.2.6 on 2021-08-13 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vps',
            name='vps_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
