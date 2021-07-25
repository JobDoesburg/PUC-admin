from django.contrib import admin

from django.contrib.admin import register
from django.utils.translation import gettext_lazy as _

from .models import Organisation, Course, User


@register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    pass


@register(Course)
class CourseAdmin(admin.ModelAdmin):
    radio_fields = {"organisation": admin.VERTICAL}

    list_display = (
        "name",
        "slug",
        "_num_schools",
    )

    def _num_schools(self, obj):
        return obj.schools.count()

    _num_schools.short_description = _("#schools")


@register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Personal",
            {"fields": ("first_name", "last_name", "email", "alternative_email",)},
        ),
        (
            "Administration",
            {
                "fields": (
                    "organisation",
                    "date_joined",
                    "last_login",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    list_display = (
        "__str__",
        "email",
        "alternative_email",
        "organisation",
        "is_active",
        "is_staff",
        "last_login",
    )

    list_filter = (
        "organisation",
        "is_active",
        "is_staff",
        "last_login",
    )

    search_fields = (
        "first_name",
        "last_name",
    )
