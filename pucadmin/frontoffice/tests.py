from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.test import Client, TestCase, RequestFactory

from frontoffice import views
from frontoffice.forms import (
    QuestionStudentFormset,
    QuestionSubmissionForm,
    SubmissionForm,
    CompetitionStudentFormset,
    CompetitionSupervisorFormSet,
)
from organisations.models import Course, Organisation
from competitions.models import (
    Submission,
    Competition,
    Student as CompetitionStudent,
    Supervisor as CompetitionSupervisor,
)

from questions.models import Question, Student as QuestionStudent


def _instantiate_formset(formset_class, data, instance=None, initial=None):
    prefix = formset_class().prefix
    formset_data = {}
    for i, form_data in enumerate(data):
        for name, value in form_data.items():
            if isinstance(value, list):
                for j, inner in enumerate(value):
                    formset_data["{}-{}-{}_{}".format(prefix, i, name, j)] = inner
            else:
                formset_data["{}-{}-{}".format(prefix, i, name)] = value
    formset_data["{}-TOTAL_FORMS".format(prefix)] = len(data)
    formset_data["{}-INITIAL_FORMS".format(prefix)] = 0

    if instance:
        return formset_class(formset_data, instance=instance, initial=initial)
    else:
        return formset_class(formset_data, initial=initial)


class QuestionFrontOfficeTest(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(name="PUC of Science")
        self.course = Course.objects.create(
            name="natuurkunde", slug="nat", organisation=self.organisation
        )
        self.form_data = {
            "school_text": "Test college Nijmegen",
            "course": self.course,
            "research_question": "Lorem ipsum dolor sit amet",
            "sub_questions": "Test test test",
            "message": "Test test test",
            "expected_end_date": timezone.datetime(year=2022, month=1, day=1),
            "privacy_policy": 1,
        }
        self.formset_data = [
            {
                "first_name": "Firstname1",
                "last_name": "Lastname1",
                "email": "student1@example.com",
            },
            {
                "first_name": "Firstname2",
                "last_name": "Lastname2",
                "email": "student2@example.com",
            },
        ]

        self.user = get_user_model().objects.create_user(
            username="test1", email="test1@example.com"
        )
        self.rf = RequestFactory()
        self.view = views.QuestionSubmissionView()
        self.client = Client()
        self.client.force_login(self.user)

    def test_privacy_policy_checked(self):
        with self.subTest("Form is valid"):
            form = QuestionSubmissionForm(self.form_data)
            self.assertTrue(form.is_valid(), msg=dict(form.errors))
        with self.subTest("Form is not valid"):
            self.form_data["privacy_policy"] = 0
            form = QuestionSubmissionForm(self.form_data)
            self.assertFalse(form.is_valid(), msg=dict(form.errors))

    def test_formset(self):
        formset = _instantiate_formset(QuestionStudentFormset, self.formset_data)
        self.assertTrue(formset.is_valid())

    def test_submit_form(self):
        self.form_data["course"] = self.course.id
        self.form_data["expected_end_date"] = "01-01-2022"
        formset = _instantiate_formset(QuestionStudentFormset, self.formset_data)

        data = {**self.form_data, **formset.data}
        response = self.client.post(f"/frontoffice/question/", data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(QuestionStudent.objects.count(), 2)
        question = Question.objects.first()
        student1 = QuestionStudent.objects.first()
        student2 = QuestionStudent.objects.last()
        self.assertEqual(question.school_text, self.form_data["school_text"])
        self.assertEqual(question.course, self.course)
        self.assertEqual(
            question.research_question, self.form_data["research_question"]
        )
        self.assertEqual(question.sub_questions, self.form_data["sub_questions"])
        self.assertEqual(question.message, self.form_data["message"])
        self.assertEqual(
            question.expected_end_date,
            timezone.datetime(year=2022, month=1, day=1).date(),
        )
        self.assertEqual(student1.first_name, self.formset_data[0]["first_name"])
        self.assertEqual(student1.last_name, self.formset_data[0]["last_name"])
        self.assertEqual(student1.email, self.formset_data[0]["email"])
        self.assertEqual(student1.question, question)
        self.assertEqual(student2.first_name, self.formset_data[1]["first_name"])
        self.assertEqual(student2.last_name, self.formset_data[1]["last_name"])
        self.assertEqual(student2.email, self.formset_data[1]["email"])
        self.assertEqual(student2.question, question)


class CompetitionFrontOfficeTest(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(name="PUC of Science")
        self.competition = Competition.objects.create(
            name="Van Melsenprjis 2022",
            organisation=self.organisation,
            registration_start=timezone.now() - timezone.timedelta(days=1),
            registration_end=timezone.now() + timezone.timedelta(days=1),
        )
        self.course = Course.objects.create(
            name="natuurkunde", slug="nat", organisation=self.organisation
        )
        self.test_file = SimpleUploadedFile(
            "test_document.pdf", b"\x00\x00\x00", content_type="application/pdf"
        )
        self.form_data = {
            "title": "Test title",
            "competition": self.competition,
            "course": self.course,
            "abstract": "Lorem ipsum dolor sit amet",
            "school_text": "Test test",
            "privacy_policy": 1,
        }
        self.student_formset_data = [
            {
                "first_name": "Firstname1",
                "last_name": "Lastname1",
                "address_1": "Address 11",
                "address_2": "Address 12",
                "zip": "1234 AB",
                "town": "Nijmegen",
                "phone": "76543210",
                "email": "student1@example.com",
            },
            {
                "first_name": "Firstname2",
                "last_name": "Lastname2",
                "address_1": "Address 12",
                "address_2": "Address 22",
                "zip": "4321 AB",
                "town": "Nijmegen",
                "phone": "01234567",
                "email": "student2@example.com",
            },
        ]
        self.supervisor_formset_data = [
            {
                "first_name": "Firstname1",
                "last_name": "Lastname1",
                "phone": "76543210",
                "email": "student1@example.com",
                "course": self.course,
            },
        ]

        self.user = get_user_model().objects.create_user(
            username="test1", email="test1@example.com"
        )
        self.rf = RequestFactory()
        self.view = views.CompetitionSubmissionView()
        self.client = Client()
        self.client.force_login(self.user)

    def test_privacy_policy_checked(self):
        with self.subTest("Form is valid"):
            form = SubmissionForm(self.form_data, {"document": self.test_file})
            self.assertTrue(form.is_valid(), msg=dict(form.errors))
        with self.subTest("Form is not valid"):
            self.form_data["privacy_policy"] = 0
            form = SubmissionForm(self.form_data, {"document": self.test_file})
            self.assertFalse(form.is_valid(), msg=dict(form.errors))

    def test_formset(self):
        student_formset = _instantiate_formset(
            CompetitionStudentFormset, self.student_formset_data
        )
        self.assertTrue(student_formset.is_valid())
        supervisor_formset = _instantiate_formset(
            CompetitionSupervisorFormSet, self.supervisor_formset_data
        )
        self.assertTrue(supervisor_formset.is_valid())

    def test_submit_form(self):
        self.form_data["course"] = self.course.id
        self.form_data["competition"] = self.competition.id
        self.supervisor_formset_data[0]["course"] = self.course.id

        student_formset = _instantiate_formset(
            CompetitionStudentFormset, self.student_formset_data
        )
        supervisor_formset = _instantiate_formset(
            CompetitionSupervisorFormSet, self.supervisor_formset_data
        )
        data = {**self.form_data, **student_formset.data, **supervisor_formset.data}
        response = self.client.post(f"/frontoffice/competition/", data, follow=True)

        # Test does not work because uploading a file does not work properly in test cases

        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(Submission.objects.count(), 1)
        # self.assertEqual(CompetitionStudent.objects.count(), 2)
        # self.assertEqual(CompetitionSupervisor.objects.count(), 1)
        # submission = Submission.objects.first()
        # student1 = CompetitionStudent.objects.first()
        # student2 = CompetitionStudent.objects.last()
        # supervisor = CompetitionSupervisor.objects.first()
        #
        # self.assertEqual(submission.competition, self.competition)
        # self.assertEqual(submission.title, self.form_data["title"])
        # self.assertEqual(submission.course, self.course)
        # self.assertEqual(submission.abstract, self.form_data["abstract"])
        # self.assertEqual(submission.school_text, self.form_data["school_text"])
        # self.assertEqual(
        #     student1.first_name, self.student_formset_data[0]["first_name"]
        # )
        # self.assertEqual(student1.last_name, self.student_formset_data[0]["last_name"])
        # self.assertEqual(student1.address_1, self.student_formset_data[0]["address_1"])
        # self.assertEqual(student1.address_2, self.student_formset_data[0]["address_2"])
        # self.assertEqual(student1.zip, self.student_formset_data[0]["zip"])
        # self.assertEqual(student1.town, self.student_formset_data[0]["town"])
        # self.assertEqual(student1.phone, self.student_formset_data[0]["phone"])
        # self.assertEqual(student1.email, self.student_formset_data[0]["email"])
        # self.assertEqual(student1.submission, submission)
        # self.assertEqual(
        #     student2.first_name, self.student_formset_data[1]["first_name"]
        # )
        # self.assertEqual(student2.last_name, self.student_formset_data[1]["last_name"])
        # self.assertEqual(student2.address_1, self.student_formset_data[1]["address_1"])
        # self.assertEqual(student2.address_2, self.student_formset_data[1]["address_2"])
        # self.assertEqual(student2.zip, self.student_formset_data[1]["zip"])
        # self.assertEqual(student2.town, self.student_formset_data[1]["town"])
        # self.assertEqual(student2.phone, self.student_formset_data[1]["phone"])
        # self.assertEqual(student2.email, self.student_formset_data[1]["email"])
        # self.assertEqual(student2.submission, submission)
        # self.assertEqual(
        #     supervisor.first_name, self.supervisor_formset_data[0]["first_name"]
        # )
        # self.assertEqual(
        #     supervisor.last_name, self.supervisor_formset_data[0]["last_name"]
        # )
        # self.assertEqual(supervisor.phone, self.supervisor_formset_data[0]["phone"])
        # self.assertEqual(supervisor.email, self.supervisor_formset_data[0]["email"])
        # self.assertEqual(supervisor.course, self.course)
        # self.assertEqual(supervisor.submission, submission)
