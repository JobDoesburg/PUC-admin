from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Organisation(models.Model):
    class Meta:
        verbose_name = _("organisation")
        verbose_name_plural = _("organisations")

    name = models.CharField(
        verbose_name=_("name"), unique=True, max_length=20, blank=False, null=False
    )

    def __str__(self):
        return self.name


class Course(models.Model):
    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    name = models.CharField(
        verbose_name=_("name"), max_length=20, unique=True, blank=False, null=False
    )
    slug = models.SlugField(
        verbose_name=_("slug"), unique=True, max_length=3, blank=False, null=False
    )

    organisation = models.ForeignKey(
        Organisation,
        verbose_name=_("organisation"),
        on_delete=models.PROTECT,
        related_name="courses",
        related_query_name="courses",
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    organisation = models.ForeignKey(
        Organisation,
        verbose_name=_("organisation"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
        related_query_name="users",
    )
    courses = models.ManyToManyField(Course, verbose_name=_("courses"))

    alternative_email = models.EmailField(
        verbose_name=_("alternative email"),
        blank=True,
        null=True,
        help_text=_(
            "Notifications for new questions for this course will be sent to this address. If empty, the default email will be used."
        ),
    )

    @property
    def notification_email(self):
        if self.alternative_email:
            return self.alternative_email
        return self.email

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
