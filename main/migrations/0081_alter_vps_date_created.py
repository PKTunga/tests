# Generated by Django 3.2.6 on 2022-12-24 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_auto_20221218_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vps',
            name='date_created',
            field=models.DateField(auto_now=True, null=True, verbose_name='Date created'),
        ),
    ]