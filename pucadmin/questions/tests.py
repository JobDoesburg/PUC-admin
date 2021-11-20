from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from organisations.models import Course, Organisation
from questions.models import Question, CourseAssignee


class QuestionModelTest(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(name="PUC of Science")
        self.assignee1 = get_user_model().objects.create_user(
            username="test1", email="test1@example.com"
        )
        self.assignee2 = get_user_model().objects.create_user(
            username="test2", email="test2@example.com"
        )
        self.course = Course.objects.create(
            name="natuurkunde", slug="nat", organisation=self.organisation
        )

    def test_set_first_assignee(self):
        self.question = Question(course=self.course)
        CourseAssignee.objects.create(assignee=self.assignee1, course=self.course)
        self.question.save()

        self.assertEqual(self.question.assignee, self.assignee1)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.assignee1.email])

    def test_change_assignee(self):
        self.question = Question(assignee=self.assignee1, course=self.course)
        self.question.save()

        self.question.assignee = self.assignee2
        self.question.save()

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, [self.assignee1.email])
        self.assertEqual(mail.outbox[1].to, [self.assignee2.email])
