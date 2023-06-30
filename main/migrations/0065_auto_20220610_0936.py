# Generated by Django 3.2.6 on 2022-06-10 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0064_auto_20220609_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellertemplates',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Total Cost'),
        ),
        migrations.AlterField(
            model_name='sellertemplates',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Cost Per Item'),
        ),
        migrations.AlterField(
            model_name='sellertemplates',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Quantity'),
        ),
    ]
