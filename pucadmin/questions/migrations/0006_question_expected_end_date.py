# Generated by Django 3.2.5 on 2021-08-06 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0005_alter_question_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="expected_end_date",
            field=models.DateField(null=True, verbose_name="expected end date"),
        ),
    ]
