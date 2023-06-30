# Generated by Django 3.2.6 on 2022-12-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0019_alter_customuser_referral_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_marketer',
            field=models.BooleanField(default=False, help_text='User is a Marketer', verbose_name='Is Marketer'),
        ),
    ]
