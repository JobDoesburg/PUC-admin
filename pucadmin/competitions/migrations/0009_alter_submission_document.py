# Generated by Django 4.0 on 2022-02-22 11:21

import competitions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0008_auto_20210803_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='document',
            field=models.FileField(max_length=500, upload_to=competitions.models.submission_upload_path, verbose_name='document'),
        ),
    ]
