from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from organisations.models import Course


class School(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100, unique=True)
    address_1 = models.CharField(verbose_name=_("address 1"), max_length=100)
    address_2 = models.CharField(  # django-doctor: disable=nullable-string-field
        verbose_name=_("address 2"), max_length=100, blank=True, null=True
    )
    zip = models.CharField(
        _("zip"),
        max_length=7,
        validators=[
            RegexValidator(
                regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                message=_("Enter zip code in this format: '1234 AB'"),
            )
        ],
    )
    town = models.CharField(verbose_name=_("town"), max_length=50)
    courses_offered = models.ManyToManyField(
        Course,
        verbose_name=_("courses"),
        related_query_name="schools",
        related_name="schools",
    )

    class Meta:
        verbose_name = _("school")
        verbose_name_plural = _("schools")

    def __str__(self):
        return f"{self.name} ({self.town})"


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
