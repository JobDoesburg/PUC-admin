from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from organisations.models import Course

from schools.models import School

from organisations.models import Organisation


class Competition(models.Model):
    class Meta:
        verbose_name = "competition"
        verbose_name_plural = "competitions"

    name = models.CharField(
        max_length=20,
        help_text="For example: Van Melsenprijs 2021",
        blank=False,
        null=False,
    )
    slug = models.SlugField(unique=True, max_length=20, blank=False, null=False)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="competitions",
        related_query_name="competitions",
    )

    registration_start = models.DateTimeField(blank=True, null=True)
    registration_end = models.DateTimeField(blank=True, null=True)

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
        verbose_name = "submission"
        verbose_name_plural = "submissions"
        unique_together = [["competition", "prize"], ["competition", "title"]]

    created_at = models.DateTimeField(auto_now_add=True)
    competition = models.ForeignKey(
        Competition,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="submissions",
        related_query_name="submissions",
    )
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=120, unique=True, blank=False, null=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="submissions",
        related_query_name="submissions",
    )
    abstract = models.TextField(blank=False, null=False)
    document = models.FileField(upload_to=submission_upload_path)
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="submissions",
        related_query_name="submissions",
    )

    nominated = models.BooleanField(default=False)
    nomination_report = models.TextField(blank=True, null=False)
    nomination_score = models.PositiveSmallIntegerField(blank=True, null=True)

    prize = models.PositiveSmallIntegerField(blank=True, null=True)
    jury_report = models.TextField(blank=True, null=True)

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
                    "course": "This course is not managed by the organisation of this competition."
                }
            )
        if errors:
            raise ValidationError(errors)

    @staticmethod
    def __stringify_persons(queryset):
        persons = queryset.order_by("last_name").all()
        if len(persons) == 0:
            return None
        elif len(persons) == 1:
            return str(persons[0])
        elif len(persons) == 2:
            return f"{persons[0]} & {persons[1]}"
        else:
            return ", ".join(persons[0:-2]) + f" & {persons[-1]}"

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
        verbose_name = "student"
        verbose_name_plural = "students"

    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    address_1 = models.CharField(max_length=100, blank=True, null=True)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                message="Enter zip code in this format: '1234 AB'",
            )
        ],
    )
    town = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="authors",
        related_query_name="authors",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Supervisor(models.Model):
    class Meta:
        verbose_name = "supervisor"
        verbose_name_plural = "supervisors"

    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    address_1 = models.CharField(max_length=100, blank=True, null=True)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^[1-9][0-9]{3} (?!SA|SD|SS)[A-Z]{2}",
                message="Enter zip code in this format: '1234 AB'",
            )
        ],
    )
    town = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="supervisors",
        related_query_name="supervisors",
    )

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="supervisors",
        related_query_name="supervisors",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
