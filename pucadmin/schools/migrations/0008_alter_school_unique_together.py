# Generated by Django 4.0 on 2022-03-14 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0007_school_location_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='school',
            unique_together={('bg_id', 'brin_id', 'location_id')},
        ),
    ]