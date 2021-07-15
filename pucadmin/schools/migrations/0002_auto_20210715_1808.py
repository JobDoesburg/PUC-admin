# Generated by Django 3.2.5 on 2021-07-15 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0003_auto_20210715_1808'),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='courses_offered',
            field=models.ManyToManyField(related_name='schools', related_query_name='schools', to='organisations.Course'),
        ),
        migrations.AlterField(
            model_name='schoolremark',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remarks', related_query_name='remarks', to='schools.school'),
        ),
    ]
