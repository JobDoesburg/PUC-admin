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
        "name",
        "town",
        "address_1",
        "address_2",
        "zip",
    ]
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    list_display_links = (
        "name",
        "town",
    )
    list_display = (
        "name",
        "town",
        "address_1",
        "address_2",
        "zip",
    )
    list_filter = (
        "town",
        "courses_offered",
    )
