# Generated by Django 3.2.6 on 2021-08-20 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_accountlogs_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Templates+', to='main.templates'),
        ),
    ]
