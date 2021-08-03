from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from organisations.models import Course

from schools.models import School

from organisations.models import Organisation


class Competition(models.Model):
    class Meta:
        verbose_name = _("competition")
        verbose_name_plural = _("competitions")

    name = models.CharField(
        verbose_name=_("name"),
        max_length=20,
        help_text=_("For example: Van Melsenprijs 2021"),
    )
    slug = models.SlugField(verbose_name=_("slug"), unique=True, max_length=20)
    organisation = models.ForeignKey(
        Organisation,
        verbose_name=_("organisation"),
        on_delete=models.PROTECT,
        related_name="competitions",
        related_query_name="competitions",
    )

    registration_start = models.DateTimeField(
        verbose_name=_("registration start"), blank=True, null=True
    )
    registration_end = models.DateTimeField(
        verbose_name=_("registration end"), blank=True, null=True
    )

    nomination_date = models.DateField(
        verbose_name=_("nomination date"),
        null=True,
        help_text=_(
            "Communicated towards students in confirmation email as the latest date they"
            " will hear about their nomination"
        ),
        blank=True,
    )

    competition_date = models.DateField(
        verbose_name=_("competition date"), null=True, blank=True
    )

    @property
    def registration_open(self):
        if self.registration_start and self.registration_end:
            return self.registration_start <= timezone.now() < self.registration_end
        elif self.registration_start and not self.registration_end:
            return self.registration_start <= timezone.now()
        return False

    @classmethod
    def open_for_registration(cls):
        return Competition.objects.filter(
            Q(registration_start__lte=timezone.now())
            & (
                Q(registration_end__gt=timezone.now())
                | Q(registration_end__isnull=True)
            )
        )

    def __str__(self):
        return self.name


def submission_upload_path(instance, filename):
    return f"{instance.competition.slug}/submission_{instance.course.slug}_{instance.slug}/{filename}"


class Submission(models.Model):
    class Meta:
        verbose_name = _("submission")
        verbose_name_plural = _("submissions")
        unique_together = [["competition", "title"]]

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    competition = models.ForeignKey(
        Competition,
        verbose_name=_("competition"),
        on_delete=models.PROTECT,
        related_name="submissions",
        related_query_name="submissions",
    )
    title = models.CharField(verbose_name=_("title"), max_length=100, unique=True)
    slug = models.SlugField(verbose_name=_("slug"), max_length=120, unique=True)
    course = models.ForeignKey(
        Course,
        verbose_name=_("course"),
        on_delete=models.PROTECT,
        related_name="submissions",
        related_query_name="submissions",
    )
    abstract = models.TextField(verbose_name=_("abstract"))
    document = models.FileField(
        verbose_name=_("document"), upload_to=submission_upload_path
    )
    school_text = models.CharField(
        verbose_name=_("school (text)"), max_length=100, blank=True, null=True
    )
    school = models.ForeignKey(
        School,
        verbose_name=_("school"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="submissions",
        related_query_name="submissions",
    )

    nominated = models.BooleanField(verbose_name=_("nominated"), default=False)
    nomination_report = models.TextField(verbose_name=_("nomination report"), blank=True)
    nomination_score = models.PositiveSmallIntegerField(
        verbose_name=_("nomination score"), blank=True, null=True
    )

    prize = models.PositiveSmallIntegerField(
        verbose_name=_("prize"), blank=True, null=True
    )
    jury_report = models.TextField(verbose_name=_("jury report"), blank=True, null=True)

    def clean(self):
        super().clean()
        errors = {}
        if (
            self.course
            not in Course.objects.filter(
                organisation=self.competition.organisation
            ).all()
        ):
            errors.update(
                {
                    "course": _(
                        "This course is not managed by the organisation of this competition."
                    )
                }
            )
        if errors:
            raise ValidationError(errors)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(force_insert, force_update, using, update_fields)

    @staticmethod
    def __stringify_persons(queryset):
        persons = list(queryset.order_by("last_name").all())
        if len(persons) == 0:
            return None
        elif len(persons) == 1:
            return str(persons[0])
        elif len(persons) == 2:
            return f"{persons[0]} & {persons[1]}"
        else:
            return (
                ", ".join([str(person) for person in persons[0:-1]])
                + f" & {persons[-1]}"
            )

    @property
    def authors_text(self):
        return self.__stringify_persons(self.authors)

    @property
    def supervisors_text(self):
        return self.__stringify_persons(self.supervisors)

    def prize_text(self):
        if self.prize:
            ordinal = lambda n: "%d%s" % (
                n,
                "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4],
            )
            if (
                self.competition.submissions.filter(prize=self.prize)
                .exclude(pk=self.pk)
                .exists()
            ):
                return f"{ordinal(self.prize)} prize ex aequo"
            return f"{ordinal(self.prize)} prize"
        return None

    def __str__(self):
        if self.prize:
            return f"{self.title} ({self.authors_text}, {self.created_at:%Y}) [{self.prize_text}]"
        return f"{self.title} ({self.authors_text}, {self.created_at:%Y})"


class Student(models.Model):
    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    first_name = models.CharField(verbose_name=_("first name"), max_length=20)
    last_name = models.CharField(verbose_name=_("last name"), max_length=20)
    address_1 = models.CharField(
        verbose_name=_("address 1"), max_length=100, blank=True, null=True
    )
    address_2 = models.CharField(
        verbose_name=_("address 2"), max_length=100, blank=True, null=True
    )
    zip = models.CharField(
        verbose_name=_("zip"),
        max_length=7,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                message=_("Enter zip code in this format: '1234 AB'"),
            )
        ],
    )
    town = models.CharField(
        verbose_name=_("town"), max_length=50, blank=True, null=True
    )
    phone = models.CharField(
        verbose_name=_("phone"), max_length=20, blank=True, null=True
    )
    email = models.EmailField(verbose_name=_("email"), blank=True, null=True)

    submission = models.ForeignKey(
        Submission,
        verbose_name=_("submission"),
        on_delete=models.CASCADE,
        related_name="authors",
        related_query_name="authors",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Supervisor(models.Model):
    class Meta:
        verbose_name = _("supervisor")
        verbose_name_plural = _("supervisors")

    first_name = models.CharField(
        verbose_name=_("first name"), max_length=20, blank=False, null=False
    )
    last_name = models.CharField(
        verbose_name=_("last name"), max_length=20, blank=False, null=False
    )
    phone = models.CharField(
        verbose_name=_("phone"), max_length=20, blank=True, null=True
    )
    email = models.EmailField(verbose_name=_("email"), blank=True, null=True)

    course = models.ForeignKey(
        Course,
        verbose_name=_("course"),
        on_delete=models.PROTECT,
        related_name="supervisors",
        related_query_name="supervisors",
    )

    submission = models.ForeignKey(
        Submission,
        verbose_name=_("submission"),
        on_delete=models.CASCADE,
        related_name="supervisors",
        related_query_name="supervisors",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
