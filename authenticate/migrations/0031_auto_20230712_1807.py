# Generated by Django 3.2.6 on 2023-07-12 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0030_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=models.CharField(max_length=30),
        ),
    ]
