from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from organisations.models import Course
from questions.services import notify_new_assignee

from schools.models import School


class CourseAssignee(models.Model):
    class Meta:
        verbose_name = _("course assignee")
        verbose_name_plural = _("course assignees")

    course = models.OneToOneField(
        Course,
        verbose_name=_("course"),
        on_delete=models.CASCADE,
        related_name="assignee",
        related_query_name="assignee",
    )
    assignee = models.ForeignKey(
        get_user_model(),
        verbose_name=_("assignee"),
        on_delete=models.PROTECT,
        related_name="assigned_courses",
        related_query_name="assigned_courses",
    )

    def __str__(self):
        return _("%(course)s assigned to %(assignee)s.") % {
            "course": self.course,
            "assignee": self.assignee,
        }


class Question(models.Model):
    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

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
    research_question = models.TextField(
        verbose_name=_("research question"), blank=True, null=True
    )
    sub_questions = models.TextField(
        verbose_name=_("sub questions"), blank=True, null=True
    )
    message = models.TextField(verbose_name=_("message"), blank=False, null=False)

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

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.assignee and self.course and hasattr(self.course, "assignee"):
            self.assignee = self.course.assignee.assignee

        try:
            old_assignee = Question.objects.get(pk=self.pk).assignee
        except models.ObjectDoesNotExist:
            old_assignee = None

        ret = super().save(force_insert, force_update, using, update_fields)

        if self.assignee and self.assignee != old_assignee:
            notify_new_assignee(self)

        return ret

    def __str__(self):
        return _("Question %(id)s (%(course)s, %(created)s)") % {
            "id": self.id,
            "course": self.course,
            "created": self.created_at.strftime("%d-%M-%Y"),
        }

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


class Student(models.Model):
    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    first_name = models.CharField(
        verbose_name=_("first name"), max_length=20, blank=False, null=False
    )
    last_name = models.CharField(
        verbose_name=_("last name"), max_length=20, blank=False, null=False
    )
    email = models.EmailField(verbose_name=_("email"), blank=True, null=True)

    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        on_delete=models.CASCADE,
        related_name="students",
        related_query_name="students",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
