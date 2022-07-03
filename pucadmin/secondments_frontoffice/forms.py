from django.forms import models, CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _

from secondments.models import Employee, TimePeriod


class EmployeeRegistrationForm(models.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "time_period",
            "name",
            "email",
            "phone",
            "study_program",
            "study_year",
            "courses",
            "hours_available",
            "dayparts",
            "public_transport",
            "drivers_license",
            "contract",
            "remarks",
        ]
        widgets = {
            "courses": CheckboxSelectMultiple,
            "dayparts": CheckboxSelectMultiple,
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["study_program"].help_text = _("What is your current study program?")
        self.fields["study_year"].help_text = _("For how many years have you been studying this study program?")
        self.fields["courses"].help_text = _("What courses are you interested in to teach?")
        self.fields["hours_available"].help_text = _("How many hours are you available per week?")
        self.fields["dayparts"].help_text = _("What dayparts are you available?")
        self.fields["public_transport"].help_text = _("Do you have a public transport subscription?")
        self.fields["drivers_license"].help_text = _("Do you have a drivers license?")
        self.fields["contract"].help_text = _("Do you already have a contract at CampusDetachering?")
        self.fields["time_period"].initial = TimePeriod.objects.last()
        self.fields["time_period"].initial = TimePeriod.objects.last()
        self.fields["email"].required = True
        self.fields["phone"].required = True
        self.fields["study_year"].required = True
        self.fields["hours_available"].required = True
