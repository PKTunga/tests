# Generated by Django 3.2.6 on 2022-09-26 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_alter_orderdetail_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='payment_status',
            field=models.CharField(blank=True, default='Pending', max_length=200, null=True),
        ),
    ]