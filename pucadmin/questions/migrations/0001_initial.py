# Generated by Django 3.2.5 on 2021-07-08 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("schools", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("organisations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("research_question", models.TextField(blank=True, null=True)),
                ("sub_questions", models.TextField(blank=True, null=True)),
                ("message", models.TextField()),
                ("completed", models.BooleanField(default=False)),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="organisations.course",
                    ),
                ),
                (
                    "school",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="questions",
                        to="schools.school",
                    ),
                ),
            ],
            options={
                "verbose_name": "question",
                "verbose_name_plural": "questions",
            },
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="students",
                        to="questions.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "student",
                "verbose_name_plural": "students",
            },
        ),
        migrations.CreateModel(
            name="CourseAssignee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "alternative_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "assignee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="assigned_courses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "course",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignee",
                        related_query_name="assignee",
                        to="organisations.course",
                    ),
                ),
            ],
            options={
                "verbose_name": "course assignee",
                "verbose_name_plural": "course assignees",
            },
        ),
    ]
