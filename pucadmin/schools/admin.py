from django.contrib import admin
from django.contrib.admin import register
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionMixin

from .models import School, SchoolRemark


class SchoolRemarkInline(admin.TabularInline):
    model = SchoolRemark
    extra = 0


class ActiveGraduatesFilter(admin.SimpleListFilter):
    title = _("active graduates")
    parameter_name = "active_graduates"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Graduates")),
            ("no", _("No graduates")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(courses_offered__isnull=False,)
        if self.value() == "no":
            return queryset.filter(courses_offered__isnull=True,)


@register(School)
class SchoolAdmin(ExportActionMixin, admin.ModelAdmin):
    inlines = [SchoolRemarkInline]
    search_fields = [
        "bg_id",
        "brin_id",
        "location_id",
        "name",
        "short_name",
        "location_town",
    ]
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    list_display = (
        "__str__",
        "location_town",
        "url",
        "location_street",
        "location_house_number",
        "location_zip",
        "in_service_region",
    )
    list_filter = (
        "in_service_region",
        ActiveGraduatesFilter,
        "courses_offered",
        "dissolved",
        "location_town",
    )
