# Generated by Django 3.2.6 on 2022-09-26 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0075_auto_20220920_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='instance_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]