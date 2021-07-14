from django.forms import models

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
        self.fields["competition"].label = "Wedstrijd"
        self.fields["competition"].queryset = Competition.open_for_registration()
        self.fields["competition"].initial = Competition.open_for_registration().first()

        self.fields["title"].label = "Titel"

        self.fields["course"].label = "Vak"
        self.fields[
            "course"
        ].help_text = "Kies het vak dat het meest van toepassing is."

        self.fields["abstract"].label = "Samenvatting"


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
        ]


class QuestionSubmissionForm(models.ModelForm):
    class Meta:
        model = Question
        fields = ["school", "course", "research_question", "sub_questions", "message"]


class QuestionStudentForm(models.ModelForm):
    class Meta:
        model = QuestionStudent
        fields = ["first_name", "last_name", "email"]
