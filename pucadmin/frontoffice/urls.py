from django.urls import path

from .views import *

app_name = "frontoffice"

urlpatterns = [
    path(
        "competition/",
        CompetitionSubmissionView.as_view(),
        name="competition-submission",
    ),
    path("question/", QuestionSubmissionView.as_view(), name="question-submission"),
]
