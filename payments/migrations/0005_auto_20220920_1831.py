# Generated by Django 3.2.6 on 2022-09-20 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0075_auto_20220920_1831'),
        ('packages', '0002_alter_packages_template'),
        ('payments', '0004_auto_20220914_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='packages.coupons', verbose_name='Coupons'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.vps', verbose_name='iNSTANCE'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='packages.packages', verbose_name='Package'),
        ),
    ]
