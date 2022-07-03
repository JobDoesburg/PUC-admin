from django.views.generic import CreateView, TemplateView

from secondments.models import Employee

from .forms import (
    EmployeeRegistrationForm,
)

class EmployeeRegistrationView(CreateView):
    model = Employee
    form_class = EmployeeRegistrationForm
    template_name = "employee_registration.html"
    success_url = "/secondments-frontoffice/registration-success"


class EmployeeRegistrationSuccessView(TemplateView):
    template_name = "employee_registration_success.html"
