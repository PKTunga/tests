# Generated by Django 3.2.6 on 2021-08-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_accountlogs_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='state',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
