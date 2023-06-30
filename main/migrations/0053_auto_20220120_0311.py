# Generated by Django 3.2.6 on 2022-01-20 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_alter_rdpfile_rdp_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='templates',
            name='generation',
            field=models.CharField(choices=[('auto', 'AUTO'), ('manual', 'MANUAL')], default='auto', max_length=20),
        ),
        migrations.AddField(
            model_name='vps',
            name='assigned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rdpfile',
            name='rdp_file',
            field=models.FileField(blank=True, default='D:\\work\\tom\\src\\rdprdp_file.rdp', max_length=254, null=True, upload_to='rdp/'),
        ),
    ]
