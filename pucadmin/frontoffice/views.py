from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt

from PUCadmin.utils import send_email
from competitions.models import Submission
from questions.models import Question

from .forms import (
    SubmissionForm,
    QuestionSubmissionForm,
    CompetitionStudentFormset,
    CompetitionSupervisorFormSet,
    QuestionStudentFormset,
)


@method_decorator(xframe_options_exempt, name="dispatch")
class CompetitionSubmissionView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "competition_submission_form.html"
    success_url = "/frontoffice/competition-success"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["students"] = CompetitionStudentFormset(self.request.POST)
            data["supervisors"] = CompetitionSupervisorFormSet(self.request.POST)
        else:
            data["students"] = CompetitionStudentFormset()
            data["supervisors"] = CompetitionSupervisorFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        students = context["students"]
        supervisors = context["supervisors"]
        if students.is_valid() and supervisors.is_valid():
            obj = form.save()
            students.instance = obj
            students.save()
            supervisors.instance = obj
            supervisors.save()

            send_email(
                (
                    list(obj.authors.values_list("email", flat=True))
                    + list(obj.supervisors.values_list("email", flat=True))
                ),
                f"Bevestiging inzending {obj.competition}",
                "email/submission-confirmation.txt",
                {"submission": obj},
            )
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(xframe_options_exempt, name="dispatch")
class QuestionSubmissionView(CreateView):
    model = Question
    form_class = QuestionSubmissionForm
    template_name = "question_submission_form.html"
    success_url = "/frontoffice/question-success"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["students"] = QuestionStudentFormset(self.request.POST)
        else:
            data["students"] = QuestionStudentFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        students = context["students"]
        if students.is_valid():
            obj = form.save()
            students.instance = obj
            students.save()

            send_email(
                list(obj.students.values_list("email", flat=True)),
                "Bevestiging PWS vraag aan Radboud Pre-University College",
                "email/question-confirmation.txt",
                {"question": obj},
            )
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class QuestionSubmissionSuccessView(TemplateView):
    template_name = "question-submission-success.html"


class CompetitionSubmissionSuccessView(TemplateView):
    template_name = "competition-submission-success.html"
