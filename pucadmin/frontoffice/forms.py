from django import forms
from django.conf import settings
from django.forms import models, inlineformset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from competitions.models import (
    Submission,
    Competition,
    Student as CompetitionStudent,
    Supervisor as CompetitionSupervisor,
)

from questions.models import Question, Student as QuestionStudent
from schools.models import School


class SubmissionForm(models.ModelForm):
    class Meta:
        model = Submission
        fields = [
            "competition",
            "title",
            "course",
            "abstract",
            "document",
            "school_text",
        ]

    privacy_policy = forms.BooleanField(required=True,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["competition"].queryset = Competition.open_for_registration()
        self.fields["competition"].initial = Competition.open_for_registration().first()
        self.fields["competition"].required = True
        self.fields["title"].required = True
        self.fields["title"].help_text = _("The title of your research")
        self.fields["course"].required = True
        self.fields["course"].help_text = _(
            "The course to which your research relates most"
        )
        self.fields["abstract"].required = True
        self.fields["abstract"].help_text = _(
            "Provide a brief summary of your research (50 to 300 words)"
        )
        self.fields["document"].required = True
        self.fields["document"].help_text = _(
            "Preferably PDF, or ZIP with additional attachments"
        )
        self.fields["school_text"].required = True
        self.fields["school_text"].label = _("School")

        self.fields["privacy_policy"].label = mark_safe(
            _(
                'The Radboud Pre-University College of Science processes the above data for the purpose of participation in the contest. The personal data will not be stored after processing. I agree with the <a href="%s" target="_blank">privacy regulations of Radboud University</a> and with the processing of the data provided by me for the purposes described above.'
            )
            % settings.PRIVACY_STATEMENT_URL
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        schools = School.objects.filter(name=self.cleaned_data["school_text"].lower())
        if schools.exists():
            instance.school = schools.first()
        if commit:
            instance.save()
        return instance


class CompetitionStudentForm(models.ModelForm):
    class Meta:
        model = CompetitionStudent
        fields = [
            "first_name",
            "last_name",
            "address_1",
            "address_2",
            "zip",
            "town",
            "phone",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["address_1"].required = True
        self.fields["zip"].required = True
        self.fields["town"].required = True
        self.fields["email"].required = True


class CompetitionSupervisorForm(models.ModelForm):
    class Meta:
        model = CompetitionSupervisor
        fields = ["first_name", "last_name", "phone", "email", "course"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["course"].required = True


CompetitionStudentFormset = inlineformset_factory(
    parent_model=Submission,
    model=CompetitionStudent,
    form=CompetitionStudentForm,
    extra=1,
    can_delete=False,
    max_num=3,
    validate_max=True,
    min_num=1,
    validate_min=True,
)

CompetitionSupervisorFormSet = inlineformset_factory(
    parent_model=Submission,
    model=CompetitionSupervisor,
    form=CompetitionSupervisorForm,
    extra=0,
    can_delete=False,
    max_num=2,
    validate_max=True,
    min_num=1,
    validate_min=True,
)


class QuestionSubmissionForm(models.ModelForm):
    class Meta:
        model = Question
        fields = [
            "school_text",
            "course",
            "research_question",
            "sub_questions",
            "message",
            "expected_end_date",
        ]
        widgets = {
            "research_question": forms.Textarea(attrs={"rows": 2,}),
            "sub_questions": forms.Textarea(attrs={"rows": 5,}),
            "message": forms.Textarea(attrs={"rows": 8,}),
        }

    privacy_policy = forms.BooleanField(required=True,)

    expected_end_date = forms.DateField(label=_("Expected end date"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school_text"].required = True
        self.fields["school_text"].label = _("School")
        self.fields["course"].required = True
        self.fields["course"].help_text = _(
            "The course to which your research relates most"
        )
        self.fields["research_question"].required = True
        self.fields["sub_questions"].required = True
        self.fields["message"].required = True
        self.fields["message"].help_text = _(
            "Try to be as specific as possible. The more clearly the question is asked, the more specifically the answer can be formulated and the faster you will receive an answer. Also clearly state your subject and research plan in the question. We can help you with the following issues: Choosing a specific topic; Arranging a meeting with an expert; Borrowing material from Radboud University; Conducting an experiment at Radboud University; Collection of literature. Of course, other questions are also welcome, we can always give advice. We're also happy to schedule a (videoconferencing) meeting to discuss things face-to-face."
        )
        self.fields["privacy_policy"].label = mark_safe(
            _(
                'The Radboud Pre-University College of Science processes the above data for the purpose of answering the questions. The personal data will not be stored after processing. I agree with the <a href="%s" target="_blank">privacy regulations of Radboud University</a> and with the processing of the data provided by me for the purposes described above.'
            )
            % settings.PRIVACY_STATEMENT_URL
        )
        self.fields["expected_end_date"].required = True
        self.fields["expected_end_date"].help_text = _(
            "DD-MM-YYYY. When do you expect to be finished with your research."
        )
        self.fields["expected_end_date"].widget.input_type = "date"

    def save(self, commit=True):
        instance = super().save(commit=False)
        schools = School.objects.filter(name=self.cleaned_data["school_text"].lower())
        if schools.exists():
            instance.school = schools.first()
        if commit:
            instance.save()
        return instance


class QuestionStudentForm(models.ModelForm):
    class Meta:
        model = QuestionStudent
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True


QuestionStudentFormset = inlineformset_factory(
    parent_model=Question,
    model=QuestionStudent,
    form=QuestionStudentForm,
    extra=1,
    can_delete=False,
    max_num=3,
    validate_max=True,
    min_num=1,
    validate_min=True,
)
