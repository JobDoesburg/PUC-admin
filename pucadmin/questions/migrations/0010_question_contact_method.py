# Generated by Django 4.1.7 on 2023-03-01 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_alter_courseassignee_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='contact_method',
            field=models.CharField(choices=[('email', 'email'), ('video_call', 'video call')], default='email', max_length=100, verbose_name='contact method'),
        ),
    ]
