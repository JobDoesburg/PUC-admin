from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from organisations.models import Course
from schools.models import School


class TimePeriod(models.Model):
    class Meta:
        verbose_name = _("time period")
        verbose_name_plural = _("time periods")

    name = models.CharField(
        verbose_name=_("name"), max_length=20, help_text=_("For example, 2019-2020")
    )

    start = models.DateField()
    end = models.DateField()

    def clean(self):
        super().clean()
        errors = {}
        if self.start > self.end:
            errors.update({"end": _("End date cannot be before start date.")})
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name


class Daypart(models.Model):
    class Meta:
        verbose_name = _("daypart")
        verbose_name_plural = _("dayparts")

    name = models.CharField(verbose_name=_("name"), max_length=20)

    def __str__(self):
        return self.name


class StudyProgram(models.Model):
    class Meta:
        verbose_name = _("study program")
        verbose_name_plural = _("study program")

    name = models.CharField(verbose_name=_("name"), max_length=20)

    def __str__(self):
        return self.name


class Employee(models.Model):
    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    time_period = models.ForeignKey(
        TimePeriod,
        verbose_name=_("time period"),
        on_delete=models.CASCADE,
        related_query_name="employees",
        related_name="employees",
    )

    name = models.CharField(
        verbose_name=_("name"),
        max_length=100,
        help_text=_(
            "Make sure the name matches the name registered at, for example, CampusDetachering."
        ),
    )
    phone = models.CharField(  # django-doctor: disable=nullable-string-field
        verbose_name=_("phone"), max_length=20, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name=_("email"), blank=True, null=True
    )  # django-doctor: disable=nullable-string-field  # django-doctor: disable=nullable-string-field

    study_program = models.ForeignKey(
        StudyProgram,
        verbose_name=_("study program"),
        on_delete=models.PROTECT,
        related_query_name="employees",
        related_name="employees",
    )
    study_year = models.PositiveSmallIntegerField(
        verbose_name=_("study year"), null=True, blank=True
    )

    courses = models.ManyToManyField(Course, verbose_name=_("courses"),)

    hours_available = models.PositiveSmallIntegerField(
        verbose_name=_("hours available"), null=True, blank=True
    )

    dayparts = models.ManyToManyField(
        Daypart,
        verbose_name=_("dayparts"),
        related_query_name="dayparts",
        related_name="dayparts",
    )

    drivers_license = models.BooleanField(verbose_name=_("drivers license"))

    WEEK_SUBSCRIPTION = "week"
    WEEKEND_SUBSCRIPTION = "weekend"

    PUBLIC_TRANSPORT_TYPES = (
        (WEEK_SUBSCRIPTION, _("Week subscription")),
        (WEEKEND_SUBSCRIPTION, _("Weekend subscription")),
    )

    public_transport = models.CharField(
        verbose_name=_("public transport"),
        max_length=10,
        choices=PUBLIC_TRANSPORT_TYPES,
        blank=True,
        null=True,
    )

    contract = models.BooleanField(verbose_name=_("contract"))

    remarks = models.TextField(verbose_name=_("remarks"), blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.time_period})"


class SecondmentSchool(models.Model):
    class Meta:
        verbose_name = _("school")
        verbose_name_plural = _("schools")

    time_period = models.ForeignKey(
        TimePeriod,
        verbose_name=_("time period"),
        on_delete=models.CASCADE,
        related_query_name="secondment_schools",
        related_name="secondment_schools",
    )
    school = models.ForeignKey(
        School,
        verbose_name=_("school"),
        on_delete=models.PROTECT,
        related_query_name="secondment_schools",
        related_name="secondment_schools",
    )
    contact_person = models.CharField(
        verbose_name=_("contact person"), max_length=100, blank=True, null=True
    )
    phone = models.CharField(  # django-doctor: disable=nullable-string-field
        verbose_name=_("phone"), max_length=20, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name=_("email"), blank=True, null=True
    )  # django-doctor: disable=nullable-string-field  # django-doctor: disable=nullable-string-field

    drivers_license_required = models.BooleanField(
        verbose_name=_("drivers license required")
    )

    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.school)} ({self.contact_person}) ({self.time_period})"


class Request(models.Model):
    class Meta:
        verbose_name = _("request")
        verbose_name_plural = _("requests")

    school = models.ForeignKey(
        SecondmentSchool,
        verbose_name=_("school"),
        on_delete=models.PROTECT,
        related_query_name="requests",
        related_name="requests",
    )

    course = models.ForeignKey(
        Course,
        verbose_name=_("course"),
        on_delete=models.PROTECT,
        related_query_name="secondment_requests",
        related_name="secondment_requests",
    )

    num_hours = models.PositiveSmallIntegerField(
        verbose_name=_("num. hours"), null=False, blank=False
    )

    dayparts = models.ManyToManyField(
        Daypart,
        verbose_name=_("dayparts"),
        related_name="requests",
        related_query_name="requests",
    )

    employee = models.ForeignKey(
        Employee,
        verbose_name=_("employee"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_query_name="secondments",
        related_name="secondments",
    )

    remarks = models.TextField(verbose_name=_("remarks"), blank=True, null=True)

    @property
    def candidates_url(self):
        url = reverse("admin:secondments_employee_changelist")
        url += "?"
        url += f"time_period__id__exact={self.school.time_period.id}"
        url += f"&courses__id__exact={self.course.id}"
        dayparts = [str(x.id) for x in self.dayparts.all()]
        url += f"&dayparts={','.join(dayparts)}"
        if self.school.drivers_license_required:
            url += "&drivers_license__exact=1"
        return url

    def __str__(self):
        return _("Secondment request for %(course)s by %(school)s.") % {
            "course": self.course,
            "school": self.school,
        }
