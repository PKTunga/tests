# Generated by Django 3.2.6 on 2021-08-21 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0004_customuser_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Delete.', verbose_name='deleted'),
        ),
    ]