from django.views.generic import CreateView

from competitions.models import Submission
from questions.models import Question

from .forms import (
    SubmissionForm,
    QuestionSubmissionForm, CompetitionStudentFormset,
    CompetitionSupervisorFormSet, QuestionStudentFormset,
)


class CompetitionSubmissionView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "competition_submission_form.html"
    success_url = "/"

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
        return super().form_valid(form)


class QuestionSubmissionView(CreateView):
    model = Question
    form_class = QuestionSubmissionForm
    template_name = "question_submission_form.html"
    success_url = "/"

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
        return super().form_valid(form)
