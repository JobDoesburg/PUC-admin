from django.forms import models, inlineformset_factory

from competitions.models import (
    Submission,
    Competition,
    Student as CompetitionStudent,
    Supervisor as CompetitionSupervisor,
)

from questions.models import Question, Student as QuestionStudent


class SubmissionForm(models.ModelForm):
    class Meta:
        model = Submission
        fields = ["competition", "title", "course", "abstract", "document", "school"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["competition"].queryset = Competition.open_for_registration()
        self.fields["competition"].initial = Competition.open_for_registration().first()
        self.fields['competition'].required = True
        self.fields['title'].required = True
        self.fields['course'].required = True
        self.fields['abstract'].required = True
        self.fields['document'].required = True
        self.fields['school'].required = True


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
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['address_1'].required = True
        self.fields['zip'].required = True
        self.fields['town'].required = True
        self.fields['email'].required = True


class CompetitionSupervisorForm(models.ModelForm):
    class Meta:
        model = CompetitionSupervisor
        fields = [
            "first_name",
            "last_name",
            "address_1",
            "address_2",
            "zip",
            "town",
            "phone",
            "email",
            "course"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['course'].required = True


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
        fields = ["school", "course", "research_question", "sub_questions", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].required = True
        self.fields['course'].required = True
        self.fields['research_question'].required = True
        self.fields['sub_questions'].required = True
        self.fields['message'].required = True


class QuestionStudentForm(models.ModelForm):
    class Meta:
        model = QuestionStudent
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

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
