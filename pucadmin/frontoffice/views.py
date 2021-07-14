from django.forms import inlineformset_factory
from django.views.generic import FormView, CreateView

from competitions.models import (
    Submission,
    Student as CompetitionStudent,
    Supervisor as CompetitionSupervisor,
)
from questions.models import Question, Student as QuestionStudent

from .forms import (
    SubmissionForm,
    QuestionSubmissionForm,
    CompetitionStudentForm,
    CompetitionSupervisorForm,
    QuestionStudentForm,
)


class CompetitionSubmissionView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submission_form.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        StudentFormset = inlineformset_factory(
            Submission,
            CompetitionStudent,
            CompetitionStudentForm,
            min_num=1,
            extra=2,
            validate_min=1,
            validate_max=3,
            can_delete=False,
        )
        SupervisorFormSet = inlineformset_factory(
            Submission,
            CompetitionSupervisor,
            CompetitionSupervisorForm,
            min_num=1,
            extra=1,
            validate_min=1,
            validate_max=2,
            can_delete=False,
        )
        if self.request.POST:
            data["students"] = StudentFormset(self.request.POST)
            data["supervisors"] = SupervisorFormSet(self.request.POST)
        else:
            data["students"] = StudentFormset()
            data["supervisors"] = SupervisorFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        students = context["students"]
        supervisors = context["supervisors"]
        self.object = form.save()
        if students.is_valid():
            students.instance = self.object
            students.save()
        if supervisors.is_valid():
            supervisors.instance = self.object
            supervisors.save()
        return super().form_valid(form)


class QuestionSubmissionView(CreateView):
    model = Question
    form_class = QuestionSubmissionForm
    template_name = "submission_form.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        StudentFormset = inlineformset_factory(
            Question,
            QuestionStudent,
            QuestionStudentForm,
            min_num=1,
            extra=2,
            validate_min=1,
            validate_max=3,
            can_delete=False,
        )
        if self.request.POST:
            data["students"] = StudentFormset(self.request.POST)
        else:
            data["students"] = StudentFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        students = context["students"]
        self.object = form.save()
        if students.is_valid():
            students.instance = self.object
            students.save()
        return super().form_valid(form)
