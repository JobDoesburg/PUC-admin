# Generated by Django 3.2.5 on 2021-07-08 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="organistation",
        ),
        migrations.AddField(
            model_name="user",
            name="organisation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="organisations.organisation",
            ),
        ),
    ]
