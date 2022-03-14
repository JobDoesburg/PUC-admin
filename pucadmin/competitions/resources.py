from import_export import resources, fields

from .models import Submission, Student, Supervisor


class SubmissionResource(resources.ModelResource):

    course = fields.Field(attribute="course__slug")
    school = fields.Field(attribute="school__name")

    class Meta:
        model = Submission
        fields = (
            "id",
            "created_at",
            "title",
            "course",
            "abstract",
            "document",
            "school",
            "nominated",
            "nomination_score",
            "prize",
            "jury_report",
            "students",
        )
        export_order = (
            "id",
            "created_at",
            "title",
            "course",
            "abstract",
            "document",
            "school",
            "nominated",
            "nomination_score",
            "prize",
            "jury_report",
            "students",
        )
        widgets = {
            "created_at": {"format": "%d-%m-%Y"},
        }


class StudentResource(resources.ModelResource):
    competition = fields.Field(attribute="submission__competition")
    submission_id = fields.Field(attribute="submission__id")
    submission = fields.Field(attribute="submission__title")
    nominated = fields.Field(attribute="submission__nominated")
    prize = fields.Field(attribute="submission__prize")
    course = fields.Field(attribute="submission__course")
    school = fields.Field(attribute="submission__school")

    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "address_1",
            "address_2",
            "zip",
            "town",
            "phone",
            "email",
        )
        export_order = (
            "id",
            "first_name",
            "last_name",
            "address_1",
            "address_2",
            "zip",
            "town",
            "phone",
            "email",
            "submission_id",
            "submission",
            "nominated",
            "prize",
            "course",
            "school",
        )


class SupervisorResource(StudentResource):

    school_correspondence_street = fields.Field(
        attribute="school__correspondence_street"
    )
    school_correspondence_house_number = fields.Field(
        attribute="school__correspondence_house_number"
    )
    school_correspondence_zip = fields.Field(attribute="school__correspondence_zip")
    school_correspondence_town = fields.Field(attribute="school__correspondence_town")

    class Meta:
        model = Supervisor
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
        )
        export_order = (
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "submission_id",
            "submission",
            "nominated",
            "prize",
            "course",
            "school",
            "school_correspondence_street",
            "school_correspondence_house_number",
            "school_correspondence_zip",
            "school_correspondence_town",
        )
