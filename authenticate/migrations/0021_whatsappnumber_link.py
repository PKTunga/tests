# Generated by Django 3.2.6 on 2022-12-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0020_customuser_is_marketer'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatsappnumber',
            name='link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
