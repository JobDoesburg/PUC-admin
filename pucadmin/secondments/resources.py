from import_export import resources

from .models import Employee, Request, SecondmentSchool


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        exclude = ()
        fields = (
            "name",
            "email",
            "phone",
            "study_program",
            "study_year",
            "drivers_license",
            "public_transport",
            "contract",
            "hours_available",
            "remarks",
        )
        export_order = fields


class SecondmentRequestResource(resources.ModelResource):
    class Meta:
        model = Request
        exclude = ()
        fields = (
            "school__time_period__name",
            "employee__name",
            "employee__email",
            "employee__phone",
            "employee__drivers_license",
            "employee__public_transport",
            "course__name",
            "num_hours",
            "school__school__name",
            "school__school__location_town",
            "school__contact_person",
            "school__email",
            "school__phone",
            "remarks",
        )
        export_order = fields


class SecondmentSchoolResource(resources.ModelResource):
    class Meta:
        model = SecondmentSchool
        exclude = ()
        fields = (
            "time_period__name",
            "school__name",
            "school__location_town",
            "contact_person",
            "phone",
            "email",
            "drivers_license_required",
            "remarks",
        )
        export_order = fields
