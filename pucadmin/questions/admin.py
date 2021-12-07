from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django.contrib import admin

from django.contrib.admin import register
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import CourseAssignee, Question, Student, Correspondence


@register(CourseAssignee)
class CourseAssigneeAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "_assignee",
    )

    def _assignee(self, obj):
        if obj.assignee:
            url = reverse("admin:organisations_user_change", args=(obj.assignee.pk,))
            return format_html("<a href='{}'>{}</a>", url, obj.assignee)

    _assignee.short_description = _("assignee")
    _assignee.admin_order_field = "assignee"


class StudentInline(admin.StackedInline):
    model = Student
    extra = 0


class CorrespondenceInline(admin.StackedInline):
    model = Correspondence
    extra = 0
    fields = (
        "date",
        "message",
    )


@register(Question)
class QuestionAdmin(AutocompleteFilterMixin, admin.ModelAdmin):
    inlines = [StudentInline, CorrespondenceInline]

    autocomplete_fields = ["school"]
    fieldsets = (
        (
            _("Administrative"),
            {
                "classes": ("",),
                "fields": (
                    "id",
                    "created_at",
                    "school_text",
                    "school",
                    "expected_end_date",
                    "assignee",
                    "completed",
                ),
            },
        ),
        (
            _("Question"),
            {
                "fields": (
                    "course",
                    "research_question",
                    "sub_questions",
                    "message",
                    "send_email",
                    "tags",
                )
            },
        ),
    )
    readonly_fields = (
        "id",
        "created_at",
        "send_email",
    )
    list_display = (
        "_created_at",
        "_students",
        "course",
        "_school",
        "research_question",
        "assignee",
        "completed",
    )
    list_display_links = (
        "_created_at",
        "_students",
        "course",
    )
    search_fields = (
        "research_question",
        "sub_questions",
        "message",
        "course",
        "school",
        "tags",
    )
    # date_hierarchy = "created_at"

    def _created_at(self, obj):
        return f"{obj.created_at:%d-%m-%Y}"

    _created_at.short_description = _("created at")
    _created_at.admin_order_field = "created_at"

    def _school(self, obj):
        if obj.school:
            url = reverse("admin:schools_school_change", args=(obj.school.pk,))
            return format_html("<a href='{}'>{}</a>", url, obj.school)

    _school.short_description = _("school")
    _school.admin_order_field = "school"

    def send_email(self, obj):
        if obj:
            return format_html(
                "<a class='button' href='mailto:{}'>{}</a>",
                obj.student_emails,
                _("Send email to students"),
            )
        return ""

    send_email.short_description = _("email")

    def _students(self, obj):
        return obj.students_text

    _students.short_description = _("students")

    list_filter = (
        "course",
        ("school", AutocompleteListFilter),
        ("assignee", AutocompleteListFilter),
        ("tags", AutocompleteListFilter),
        "completed",
        "created_at",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.has_perm("questions.view_unassigned"):
            queryset = queryset.filter(
                Q(assignee=request.user)
                | Q(course__in=request.user.assigned_courses.values("course"))
            )

        return queryset

    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.has_perm("questions.complete_question"):
            return True
        return super().has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))

        if not request.user.has_perm("questions.change_question"):
            fields += [f.name for f in self.model._meta.fields]

            if request.user.has_perm("questions.complete_question"):
                fields.remove("completed")

            if request.user.has_perm("questions.change_assignee"):
                fields.remove("assignee")

            if obj:
                fields.remove("school")

        return fields
