from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django.contrib import admin

from django.contrib.admin import register
from django.urls import reverse
from django.utils.html import format_html

from .models import CourseAssignee, Question, Student


@register(CourseAssignee)
class CourseAssigneeAdmin(admin.ModelAdmin):
    list_display = ("course", "_assignee",)

    def _assignee(self, obj):
        if obj.assignee:
            url = reverse("admin:organisations_user_change", args=(obj.assignee.pk,))
            return format_html("<a href='{}'>{}</a>", url, obj.assignee)

    _assignee.short_description = "assignee"
    _assignee.admin_order_field = "assignee"


class StudentSubmissionInline(admin.StackedInline):
    model = Student
    extra = 0


@register(Question)
class QuestionAdmin(AutocompleteFilterMixin, admin.ModelAdmin):
    inlines = [StudentSubmissionInline]

    autocomplete_fields = ["school"]
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
    )
    date_hierarchy = "created_at"

    def _created_at(self, obj):
        return f"{obj.created_at:%d-%m-%Y}"

    _created_at.short_description = "created at"
    _created_at.admin_order_field = "created_at"

    def _school(self, obj):
        if obj.school:
            url = reverse("admin:schools_school_change", args=(obj.school.pk,))
            return format_html("<a href='{}'>{}</a>", url, obj.school)

    _school.short_description = "school"
    _school.admin_order_field = "school"

    def _students(self, obj):
        return obj.students_text

    _students.short_description = "students"

    list_filter = (
        "course",
        ("school", AutocompleteListFilter),
        ("assignee", AutocompleteListFilter),
        "completed",
        "created_at",
    )
