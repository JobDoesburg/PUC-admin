from django.urls import path

from .views import *

app_name = "secondments-frontoffice"

urlpatterns = [
    path(
        "register/",
        EmployeeRegistrationView.as_view(),
        name="employee-registration",
    ),
    path(
        "registration-success/",
        EmployeeRegistrationSuccessView.as_view(),
        name="employee-registration-success",
    ),
]
