from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompetitionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "competitions"
    verbose_name = _("Competitions")
