# Generated by Django 3.2.6 on 2022-06-10 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0065_auto_20220610_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='templates',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]