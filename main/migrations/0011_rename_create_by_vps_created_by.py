# Generated by Django 3.2.6 on 2021-08-18 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_vps_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vps',
            old_name='create_by',
            new_name='created_by',
        ),
    ]
