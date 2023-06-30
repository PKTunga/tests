# Generated by Django 3.2.6 on 2022-05-24 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0061_rename_create_by_sellertemplates_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellertemplates',
            name='template',
        ),
        migrations.AddField(
            model_name='sellertemplates',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Templates+', to='main.templates', verbose_name='Templates'),
        ),
    ]