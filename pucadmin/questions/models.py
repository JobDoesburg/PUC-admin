from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone

from organisations.models import Course

from schools.models import School


class CourseAssignee(models.Model):
    class Meta:
        verbose_name = "course assignee"
        verbose_name_plural = "course assignees"

    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name="assignee",
        related_query_name="assignee",
    )
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="assigned_courses",
        related_query_name="assigned_courses",
    )

    alternative_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Notifications for new questions for this course will be sent to this address. If empty, the user email of the assignee will be used.",
    )

    @property
    def notification_email(self):
        if self.alternative_email:
            return self.alternative_email
        return self.assignee.email

    def __str__(self):
        return f"{self.course} assigned to {self.assignee}"


def _notify_new_assignee(question):
    if question.course.assignee.assignee == question.assignee:
        email = question.course.assignee.notification_email
    else:
        email = question.assignee.email

    subject = f"[PUC admin] A new question {question.id} was assigned to you"
    message = f"You were assigned a question by PUC admin.\n" \
              f"The question was submitted at {question.created_at:%d-%m-%Y %H:%M} " \
              f"for the course {question.course.name} by " \
              f"{question.students_text} ({question.school}) " \
              f"and assigned to you at {timezone.now():%d-%m-%Y %H:%M}:" \
              f"\n\n\t{question.message}\n\n" \
              f"Research question:\n\t{question.research_question}\n\n" \
              f"Sub questions:\n\t{question.sub_questions}\n\n" \
              f"Do not forget to mark this question as `completed` when it has been answered!\n\n" \
              f"_This email was sent automatically_"
    send_mail(subject, message, from_email=settings.EMAIL_DEFAULT_SENDER, recipient_list=[email])

class Question(models.Model):
    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"

    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="questions",
        related_query_name="questions",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="questions",
        related_query_name="questions",
    )
    research_question = models.TextField(blank=True, null=True)
    sub_questions = models.TextField(blank=True, null=True)
    message = models.TextField(blank=False, null=False)

    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="assigned_questions",
        related_query_name="assigned_questions",
    )

    completed = models.BooleanField(default=False)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.assignee:
            self.assignee = self.course.assignee.assignee

        old_assignee = Question.objects.get(pk=self.pk).assignee
        ret = super().save(force_insert, force_update, using, update_fields)

        if self.assignee != old_assignee:
            _notify_new_assignee(self)

        return ret

    def __str__(self):
        return f"Question {self.id} ({self.course}, {self.created_at:%d-%m-%Y})"

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
    def students_text(self):
        return self.__stringify_persons(self.students)


class Student(models.Model):
    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"

    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="students",
        related_query_name="students",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
