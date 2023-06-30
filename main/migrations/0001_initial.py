# Generated by Django 3.2.6 on 2021-08-13 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VPS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_type', models.CharField(choices=[('vps', 'VPS'), ('proxy', 'PROXY')], max_length=20)),
                ('aws_account_id', models.CharField(max_length=50)),
                ('instance_id', models.CharField(max_length=50)),
                ('vps_name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Custom User+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
