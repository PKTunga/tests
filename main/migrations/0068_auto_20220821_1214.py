# Generated by Django 3.2.6 on 2022-08-21 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0067_auto_20220623_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('title', models.CharField(default='', max_length=200)),
                ('features', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='csvfile',
            name='csv_file',
            field=models.FileField(blank=True, default='D:\\work\\tom\\tom_aberdare\\rdprdp_file.rdp', max_length=254, null=True, upload_to='csv/'),
        ),
        migrations.AlterField(
            model_name='rdpfile',
            name='rdp_file',
            field=models.FileField(blank=True, default='D:\\work\\tom\\tom_aberdare\\rdprdp_file.rdp', max_length=254, null=True, upload_to='rdp/'),
        ),
    ]
