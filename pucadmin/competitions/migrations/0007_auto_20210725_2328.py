# Generated by Django 3.2.5 on 2021-07-25 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("competitions", "0006_competition_nomination_date"),
    ]

    operations = [
        migrations.RemoveField(model_name="supervisor", name="address_1",),
        migrations.RemoveField(model_name="supervisor", name="address_2",),
        migrations.RemoveField(model_name="supervisor", name="town",),
        migrations.RemoveField(model_name="supervisor", name="zip",),
    ]
