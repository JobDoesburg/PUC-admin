from django.core.validators import RegexValidator
from django.db import models

from organisations.models import Course


class School(models.Model):
    class Meta:
        verbose_name = "school"
        verbose_name_plural = "schools"

    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    address_1 = models.CharField(max_length=100, blank=False, null=False)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(
        max_length=7,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                message="Enter zip code in this format: '1234 AB'",
            )
        ],
    )
    town = models.CharField(max_length=50, blank=False, null=False)
    courses_offered = models.ManyToManyField(
        Course, related_query_name="schools", related_name="schools"
    )

    def __str__(self):
        return f"{self.name} ({self.town})"


class SchoolRemark(models.Model):
    class Meta:
        verbose_name = "remark"
        verbose_name_plural = "remarks"

    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_query_name="remarks",
        related_name="remarks",
    )
    remark = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"Remark on {self.school} at {self.created_at:%d-%M-%Y}"
