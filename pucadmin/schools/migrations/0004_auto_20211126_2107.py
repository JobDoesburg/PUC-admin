# Generated by Django 3.2.5 on 2021-11-26 20:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0003_auto_20210718_1147"),
    ]

    operations = [
        migrations.RenameField(
            model_name="school",
            old_name="town",
            new_name="location_town",
        ),
        migrations.AddField(
            model_name="school",
            name="bg_id",
            field=models.CharField(
                default=0, max_length=5, verbose_name="Bevoegd Gezag id"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="school",
            name="brin_id",
            field=models.CharField(default=0, max_length=6, verbose_name="BRIN id"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="school",
            name="correspondence_house_number",
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                verbose_name="house number (correspondence)",
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="correspondence_street",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="street (correspondence)",
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="correspondence_town",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="town (correspondence)",
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="correspondence_zip",
            field=models.CharField(
                blank=True,
                max_length=7,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Enter zip code in this format: '1234 AB'",
                        regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                    )
                ],
                verbose_name="zip",
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="dissolved",
            field=models.BooleanField(default=False, verbose_name="dissolved"),
        ),
        migrations.AddField(
            model_name="school",
            name="location_house_number",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="house number"
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="location_street",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="street"
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="location_zip",
            field=models.CharField(
                blank=True,
                max_length=7,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Enter zip code in this format: '1234 AB'",
                        regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                    )
                ],
                verbose_name="zip",
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="phone",
            field=models.CharField(
                blank=True, max_length=15, null=True, verbose_name="phone"
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="short_name",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="short name"
            ),
        ),
        migrations.AddField(
            model_name="school",
            name="url",
            field=models.URLField(blank=True, null=True, verbose_name="url"),
        ),
        migrations.AlterField(
            model_name="school",
            name="name",
            field=models.CharField(max_length=100, verbose_name="name"),
        ),
        migrations.AlterUniqueTogether(
            name="school",
            unique_together={("bg_id", "brin_id")},
        ),
        migrations.RemoveField(
            model_name="school",
            name="address_1",
        ),
        migrations.RemoveField(
            model_name="school",
            name="address_2",
        ),
        migrations.RemoveField(
            model_name="school",
            name="zip",
        ),
    ]
