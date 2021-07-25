from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django.contrib import admin
from django.contrib.admin import register
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import (
    ExportMixin,
    ImportMixin,
    ImportExportMixin,
    ExportActionMixin,
)
from django.utils.translation import gettext_lazy as _

from .models import Competition, Student, Supervisor, Submission
from .resources import SubmissionResource, StudentResource, SupervisorResource


class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0
    ordering = ["prize", "nominated", "created_at"]

    fields = [
        "title",
        "authors",
        "supervisors",
        "school",
        "course",
        "nominated",
        "prize",
    ]

    readonly_fields = ["authors", "supervisors", "prize"]

    def authors(self, obj):
        return obj.authors_text

    def supervisors(self, obj):
        return obj.supervisors_text

    def prize(self, obj):
        return obj.prize_text

    show_change_link = True
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    radio_fields = {"organisation": admin.VERTICAL}
    inlines = [SubmissionInline]
    list_display = (
        "name",
        "competition_date",
        "_registration_open",
        "_num_submissions",
    )
    list_filter = ("organisation",)
    search_fields = ("name",)

    def _num_submissions(self, obj):
        return obj.submissions.count()

    _num_submissions.short_description = _("#submissions")

    def _registration_open(self, obj):
        return obj.registration_open

    _registration_open.short_description = _("registration open")
    _registration_open.boolean = True


@register(Student)
class StudentAdmin(AutocompleteFilterMixin, ExportActionMixin, admin.ModelAdmin):
    resource_class = StudentResource
    list_display = (
        "first_name",
        "last_name",
        "email",
        "_school",
        "_competition",
        "_course",
        "_submission_title",
        "_nominated",
        "_prize",
    )
    list_select_related = ("submission",)
    list_display_links = (
        "first_name",
        "last_name",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        ("submission__competition", AutocompleteListFilter),
        ("submission", AutocompleteListFilter),
        ("submission__nominated", admin.BooleanFieldListFilter),
        "submission__prize",
        "submission__course",
        ("submission__school", AutocompleteListFilter),
    )

    def _school(self, obj):
        if obj.submission and obj.submission.school:
            url = reverse(
                "admin:schools_school_change", args=(obj.submission.school.pk,)
            )
            return format_html("<a href='{}'>{}</a>", url, obj.submission.school)

    _school.short_description = _("school")
    _school.admin_order_field = "submission__school"

    def _competition(self, obj):
        return obj.submission.competition

    _competition.short_description = _("competition")
    _competition.admin_order_field = "submission__competition"

    def _submission_title(self, obj):
        if obj.submission:
            url = reverse(
                "admin:competitions_submission_change", args=(obj.submission.pk,)
            )
            return format_html("<a href='{}'>{}</a>", url, obj.submission.title)

    _submission_title.short_description = _("title")
    _submission_title.admin_order_field = "submission__title"

    def _nominated(self, obj):
        return obj.submission.nominated

    _nominated.short_description = _("nominated")
    _nominated.boolean = True
    _nominated.admin_order_field = "submission__nominated"

    def _prize(self, obj):
        return obj.submission.prize

    _prize.short_description = _("prize")
    _prize.admin_order_field = "submission__prize"

    def _course(self, obj):
        return obj.submission.course

    _course.short_description = _("course")
    _course.admin_order_field = "submission__course"


@register(Supervisor)
class SupervisorAdmin(StudentAdmin):
    resource_class = SupervisorResource

    list_display = (
        "first_name",
        "last_name",
        "course",
        "email",
        "_school",
        "_competition",
        "_course",
        "_submission_title",
        "_nominated",
        "_prize",
    )
    list_filter = (
        "course",
        ("submission__competition", AutocompleteListFilter),
        ("submission", AutocompleteListFilter),
        ("submission__nominated", admin.BooleanFieldListFilter),
        "submission__prize",
        "submission__course",
        ("submission__school", AutocompleteListFilter),
    )


class StudentSubmissionInline(admin.StackedInline):
    model = Student
    extra = 0


class SupervisorSubmissionInline(admin.StackedInline):
    model = Supervisor
    extra = 0


@register(Submission)
class SubmissionAdmin(AutocompleteFilterMixin, ExportActionMixin, admin.ModelAdmin):
    resource_class = SubmissionResource
    inlines = [StudentSubmissionInline, SupervisorSubmissionInline]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["school"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "created_at",
                    "competition",
                    "title",
                    "slug",
                    "course",
                    "abstract",
                    "document",
                    "school_text",
                    "school",
                )
            },
        ),
        (
            "Nomimation",
            {
                "classes": ("collapse",),
                "fields": ("nominated", "nomination_score", "nomination_report",),
            },
        ),
        ("Jury", {"classes": ("collapse",), "fields": ("prize", "jury_report",),},),
    )
    readonly_fields = ("created_at",)

    list_display = (
        "title",
        "_authors",
        "_school",
        "_supervisors",
        "course",
        "_competition",
        "nominated",
        "prize",
    )
    list_select_related = (
        "competition",
        "school",
    )
    search_fields = (
        "title",
        "abstract",
        "course",
        "school",
    )
    list_filter = (
        ("competition", AutocompleteListFilter),
        "competition__organisation",
        "course",
        ("school", AutocompleteListFilter),
        ("nominated", admin.BooleanFieldListFilter),
        "prize",
    )

    def _created_at(self, obj):
        return f"{obj.created_at:%d-%m-%Y}"

    _created_at.short_description = _("created at")
    _created_at.admin_order_field = "created_at"

    def _authors(self, obj):
        return obj.authors_text

    _authors.short_description = _("authors")

    def _supervisors(self, obj):
        return obj.supervisors_text

    _supervisors.short_description = _("supervisors")

    def _school(self, obj):
        if obj.school:
            url = reverse("admin:schools_school_change", args=(obj.school.pk,))
            return format_html("<a href='{}'>{}</a>", url, obj.school)

    _school.short_description = _("school")
    _school.admin_order_field = "school"

    def _competition(self, obj):
        if obj.competition:
            url = reverse(
                "admin:competitions_competition_change", args=(obj.competition.pk,)
            )
            return format_html("<a href='{}'>{}</a>", url, obj.competition)

    _competition.short_description = _("competition")
    _competition.admin_order_field = "competition"
