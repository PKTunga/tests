# Generated by Django 3.2.6 on 2021-08-15 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_templates'),
    ]

    operations = [
        migrations.AddField(
            model_name='templates',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]
