from django.db import models
from django.contrib.auth.models import AbstractUser


class Organisation(models.Model):
    class Meta:
        verbose_name = "organisation"
        verbose_name_plural = "organisations"

    name = models.CharField(unique=True, max_length=20, blank=False, null=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"

    name = models.CharField(max_length=20, unique=True, blank=False, null=False)
    slug = models.SlugField(unique=True, max_length=3, blank=False, null=False)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        related_name="courses",
        related_query_name="courses",
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
        related_query_name="users",
    )
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
