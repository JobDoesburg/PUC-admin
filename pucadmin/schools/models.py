from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from organisations.models import Course


class School(models.Model):
    bg_id = models.CharField(verbose_name=_("Bevoegd Gezag id"), max_length=5,)
    brin_id = models.CharField(verbose_name=_("BRIN id"), max_length=6,)
    location_id = models.CharField(verbose_name=_("location id"), max_length=10)
    name = models.CharField(verbose_name=_("name"), max_length=100)
    short_name = models.CharField(
        verbose_name=_("short name"), max_length=100, blank=True, null=True
    )
    location_street = models.CharField(
        verbose_name=_("street"), max_length=100, blank=True, null=True
    )
    location_house_number = models.CharField(
        verbose_name=_("house number"), max_length=10, blank=True, null=True
    )
    location_zip = models.CharField(
        _("zip"),
        max_length=7,
        validators=[
            RegexValidator(
                regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                message=_("Enter zip code in this format: '1234 AB'"),
            )
        ],
        blank=True,
        null=True,
    )
    location_town = models.CharField(verbose_name=_("town"), max_length=50)
    correspondence_street = models.CharField(
        verbose_name=_("street (correspondence)"), max_length=100, blank=True, null=True
    )
    correspondence_house_number = models.CharField(
        verbose_name=_("house number (correspondence)"),
        max_length=10,
        blank=True,
        null=True,
    )
    correspondence_zip = models.CharField(
        _("zip"),
        max_length=7,
        validators=[
            RegexValidator(
                regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                message=_("Enter zip code in this format: '1234 AB'"),
            )
        ],
        blank=True,
        null=True,
    )
    correspondence_town = models.CharField(
        verbose_name=_("town (correspondence)"), max_length=50, blank=True, null=True
    )

    phone = models.CharField(
        verbose_name=_("phone"), max_length=15, blank=True, null=True
    )
    url = models.URLField(verbose_name=_("url"), blank=True, null=True)
    courses_offered = models.ManyToManyField(
        Course,
        verbose_name=_("courses"),
        related_query_name="schools",
        related_name="schools",
        blank=True,
    )

    dissolved = models.BooleanField(verbose_name=_("dissolved"), default=False)

    in_service_region = models.BooleanField(
        verbose_name=_("in service region"),
        help_text=_(
            "Is this school considered to be located within our service region (normally, this is determined based on zip code)?"
        ),
        default=False,
    )

    class Meta:
        verbose_name = _("school")
        verbose_name_plural = _("schools")
        unique_together = ["bg_id", "brin_id", "location_id"]

    def __str__(self):
        if self.short_name:
            return self.short_name
        return self.name


class SchoolRemark(models.Model):
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    school = models.ForeignKey(
        School,
        verbose_name=_("school"),
        on_delete=models.CASCADE,
        related_query_name="remarks",
        related_name="remarks",
    )
    remark = models.TextField(verbose_name=_("remark"))

    class Meta:
        verbose_name = _("remark")
        verbose_name_plural = _("remarks")

    def __str__(self):
        return _("Remark on %(school)s at %(created)s.") % {
            "school": self.school,
            "created": self.created_at.strftime("%d-%M-%Y"),
        }
