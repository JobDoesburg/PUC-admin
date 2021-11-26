from django.contrib import admin
from django.contrib.admin import register
from django.db import models
from django.forms import CheckboxSelectMultiple
from import_export.admin import ExportActionMixin

from .models import School, SchoolRemark


class SchoolRemarkInline(admin.TabularInline):
    model = SchoolRemark
    extra = 0


@register(School)
class SchoolAdmin(ExportActionMixin, admin.ModelAdmin):
    inlines = [SchoolRemarkInline]
    search_fields = [
        "bg_id",
        "brin_id",
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
    )
    list_filter = (
        "courses_offered",
        "dissolved",
        "location_town",
    )
