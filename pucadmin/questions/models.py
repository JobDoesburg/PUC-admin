from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from taggit_selectize.managers import TaggableManager

from organisations.models import Course
from questions.services import notify_new_assignee

from schools.models import School


class CourseAssignee(models.Model):
    course = models.ForeignKey(
        Course,
        verbose_name=_("course"),
        on_delete=models.CASCADE,
        related_name="assignees",
        related_query_name="assignees",
    )
    assignee = models.ForeignKey(
        get_user_model(),
        verbose_name=_("assignee"),
        on_delete=models.PROTECT,
        related_name="assigned_courses",
        related_query_name="assigned_courses",
    )

    class Meta:
        verbose_name = _("course assignee")
        verbose_name_plural = _("course assignees")

    def __str__(self):
        return _("%(course)s assigned to %(assignee)s.") % {
            "course": self.course,
            "assignee": self.assignee,
        }


class Question(models.Model):
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    school_text = models.CharField(  # django-doctor: disable=nullable-string-field
        verbose_name=_("school (text)"), max_length=100, blank=True, null=True
    )
    school = models.ForeignKey(
        School,
        verbose_name=_("school"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="questions",
        related_query_name="questions",
    )

    course = models.ForeignKey(
        Course,
        verbose_name=_("course"),
        on_delete=models.PROTECT,
        related_name="questions",
        related_query_name="questions",
    )
    research_question = models.TextField(  # django-doctor: disable=nullable-string-field
        verbose_name=_("research question"), blank=True, null=True
    )
    sub_questions = models.TextField(  # django-doctor: disable=nullable-string-field
        verbose_name=_("sub questions"), blank=True, null=True
    )
    message = models.TextField(verbose_name=_("message"))

    tags = TaggableManager(blank=True)

    assignee = models.ForeignKey(
        get_user_model(),
        verbose_name=_("assignee"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="assigned_questions",
        related_query_name="assigned_questions",
    )

    completed = models.BooleanField(verbose_name=_("completed"), default=False)

    expected_end_date = models.DateField(verbose_name=_("expected end date"), null=True)

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")
        permissions = [
            ("view_unassigned", _("Can view questions not assigned to that user")),
            ("complete_question", _("Can change the completion status of questions")),
            ("change_assignee", _("Can change the assignee of questions")),
        ]

    def __str__(self):
        return _("Question %(id)s (%(course)s, %(created)s)") % {
            "id": self.id,
            "course": self.course,
            "created": self.created_at.strftime("%d-%M-%Y"),
        }

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.assignee and self.course and hasattr(self.course, "assignees"):
            self.assignee = self.course.assignees.all().first().assignee

        try:
            old_assignee = Question.objects.get(pk=self.pk).assignee
        except models.ObjectDoesNotExist:
            old_assignee = None

        ret = super().save(force_insert, force_update, using, update_fields)

        if self.assignee and self.assignee != old_assignee:
            notify_new_assignee(self)

        return ret

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
    def students_text(self):
        return self.__stringify_persons(self.students)

    @property
    def student_emails(self):
        return ",".join(self.students.values_list("email", flat=True))


class Student(models.Model):
    first_name = models.CharField(verbose_name=_("first name"), max_length=20)
    last_name = models.CharField(verbose_name=_("last name"), max_length=20)
    email = models.EmailField(
        verbose_name=_("email"), blank=True, null=True
    )  # django-doctor: disable=nullable-string-field

    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        on_delete=models.CASCADE,
        related_name="students",
        related_query_name="students",
    )

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Correspondence(models.Model):
    class Meta:
        verbose_name = _("correspondence")
        verbose_name_plural = _("correspondence")

    date = models.DateField(verbose_name=_("date"), default=timezone.now)
    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        on_delete=models.CASCADE,
        related_name="correspondence",
        related_query_name="correspondence",
    )
    message = models.TextField(verbose_name=_("message"))

    def __str__(self):
        return _("Correspondence for %(question)s on %(date)s.") % {
            "question": self.question,
            "date": self.date.strftime("%d-%M-%Y"),
        }
