from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django import forms
from django.contrib import admin
from django.contrib.admin import register, EmptyFieldListFilter
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import CheckboxSelectMultiple
from django.utils.html import format_html
from import_export.admin import ExportActionMixin
from django.utils.translation import gettext_lazy as _

from secondments.models import (
    SecondmentSchool,
    Employee,
    Request,
    Daypart,
    StudyProgram,
    TimePeriod,
)
from secondments.resources import (
    EmployeeResource,
    SecondmentRequestResource,
    SecondmentSchoolResource,
)


@register(Daypart)
class DaypartAdmin(admin.ModelAdmin):
    pass


@register(StudyProgram)
class StudyProgramAdmin(admin.ModelAdmin):
    pass


@register(TimePeriod)
class TimePeriodAdmin(admin.ModelAdmin):
    pass


class SecondmentInline(admin.TabularInline):
    model = Request
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
        models.TextField: {"widget": forms.Textarea(attrs={"rows": 3, "cols": 20,})},
    }


class DaypartsFilter(admin.SimpleListFilter):
    title = _("dayparts")
    parameter_name = "dayparts"

    def lookups(self, request, model_admin):
        return Daypart.objects.values_list("id", "name")

    def selected_values(self):
        return str(self.value()).split(",") if self.value() is not None else []

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            new_values = self.selected_values().copy()
            if str(lookup) in self.selected_values():
                new_values.remove(str(lookup))
                yield {
                    "selected": True,
                    "query_string": changelist.get_query_string(
                        {self.parameter_name: ",".join(new_values)}
                    )
                    if len(new_values) > 0
                    else changelist.get_query_string(remove={self.parameter_name}),
                    "display": title,
                }
            else:
                new_values.append(str(lookup))
                yield {
                    "selected": False,
                    "query_string": changelist.get_query_string(
                        {self.parameter_name: ",".join(new_values)}
                    ),
                    "display": title,
                }

    def queryset(self, request, queryset):
        for val in self.selected_values():
            queryset = queryset.filter(dayparts__in=val)
        return queryset


@register(Employee)
class EmployeeAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = EmployeeResource
    inlines = [SecondmentInline]
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    search_fields = (
        "name",
        "study_program",
    )
    list_display = (
        "name",
        "study_program",
        "study_year",
        "drivers_license",
        "public_transport",
        "contract",
        "num_secondments",
        "hours_available",
        "hours_fulfilled",
        "hours_unfulfilled",
        "remarks",
    )
    list_display_links = ("name",)
    list_filter = (
        "time_period",
        "study_program",
        "study_year",
        "courses",
        DaypartsFilter,
        "drivers_license",
        "public_transport",
        "contract",
        ("secondments__school__school", AutocompleteListFilter),
    )

    def num_secondments(self, obj):
        if obj:
            return obj.secondments.count()
        return None

    num_secondments.short_description = _("secondments")
    num_secondments.admin_order_field = "secondments"

    def hours_fulfilled(self, obj):
        if obj:
            return obj.secondments.aggregate(fulfilled=Sum("num_hours"))["fulfilled"]
        return None

    hours_fulfilled.short_description = _("hours fulfilled")

    def hours_unfulfilled(self, obj):
        if obj and obj.hours_available:
            return (
                obj.hours_available
                - obj.secondments.aggregate(fulfilled=Coalesce(Sum("num_hours"), 0))[
                    "fulfilled"
                ]
            )
        return None

    hours_unfulfilled.short_description = _("hours unfulfilled")


class RequestInline(admin.TabularInline):
    model = Request
    extra = 0
    autocomplete_fields = ("employee",)
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
        models.TextField: {"widget": forms.Textarea(attrs={"rows": 3, "cols": 20,})},
    }

    fields = (
        "course",
        "num_hours",
        "dayparts",
        "remarks",
        "employee",
        "candidates_url",
    )
    readonly_fields = ("candidates_url",)

    def candidates_url(self, obj):
        if obj:
            return format_html(
                "<a class='button' href='{}'>{}</a>",
                obj.candidates_url,
                _("view candidates"),
            )

    candidates_url.short_description = _("candidates")


@register(SecondmentSchool)
class SecondmentSchoolAdmin(
    AutocompleteFilterMixin, ExportActionMixin, admin.ModelAdmin
):
    resource_class = SecondmentSchoolResource
    inlines = [RequestInline]
    list_display = (
        "school",
        "contact_person",
        "phone",
        "email",
        "num_requests",
        "num_requests_fulfilled",
        "num_requests_unfulfilled",
        "remarks",
    )
    search_fields = (
        "school",
        "contact_person",
        "school__location_town",
    )
    autocomplete_fields = ("school",)
    list_display_links = ("school",)
    list_filter = (
        "time_period",
        ("school", AutocompleteListFilter),
        "drivers_license_required",
    )

    def num_requests(self, obj):
        if obj:
            return obj.requests.count()
        return None

    num_requests.short_description = _("#requests")

    def num_requests_fulfilled(self, obj):
        if obj:
            return obj.requests.filter(employee__isnull=False).count()
        return None

    num_requests_fulfilled.short_description = _("#fulfilled")

    def num_requests_unfulfilled(self, obj):
        if obj:
            return obj.requests.filter(employee__isnull=True).count()
        return None

    num_requests_unfulfilled.short_description = _("#unfulfilled")


@register(Request)
class SecondmentRequestAdmin(
    AutocompleteFilterMixin, ExportActionMixin, admin.ModelAdmin
):
    resource_class = SecondmentRequestResource
    search_fields = (
        "school__school__name",
        "school__contact_person",
        "employee",
        "school__school__location_town",
    )
    readonly_fields = ("candidates_url",)
    list_display = (
        "course",
        "num_hours",
        "_location",
        "_school",
        "candidates_url",
        "employee",
        "remarks",
    )
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    list_display_links = ("course",)
    list_filter = (
        "school__time_period",
        ("employee", AutocompleteListFilter),
        ("employee", EmptyFieldListFilter),
        ("school__school", AutocompleteListFilter),
        DaypartsFilter,
    )

    def _location(self, obj):
        return obj.school.school.location_town

    _location.short_description = _("town")
    _location.admin_order_field = "school__school__location_town"

    def _school(self, obj):
        return obj.school.school

    _school.short_description = _("school")
    _school.admin_order_field = "school__school"

    def candidates_url(self, obj):
        if obj:
            return format_html(
                "<a class='button' href='{}'>{}</a>",
                obj.candidates_url,
                _("candidates"),
            )

    candidates_url.short_description = _("candidates")
