from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils import timezone

import competitions.management.commands.minimisecompetitionsdata
import questions.management.commands.minimisequestionsdata
import secondments.management.commands.minimisesecondmentssdata


def minimise_users():
    one_year_ago = timezone.now() - timezone.timedelta(days=2 * 365)
    yesterday = timezone.now() - timezone.timedelta(days=1)
    inactive_users = get_user_model().objects.filter(last_login__lt=one_year_ago)
    unauthorized_users = get_user_model().objects.filter(
        organisation__isnull=True, last_login__lt=yesterday
    )
    deleted1, _ = inactive_users.exclude(is_superuser=True).delete()
    deleted2, _ = unauthorized_users.exclude(is_superuser=True).delete()
    return deleted1 + deleted2


def minimise_data():
    minimised = questions.management.commands.minimisequestionsdata.minimise_data()
    minimised += (
        competitions.management.commands.minimisecompetitionsdata.minimise_data()
    )
    minimised += (
        secondments.management.commands.minimisesecondmentssdata.minimise_data()
    )
    minimised += minimise_users()
    return minimised


class Command(BaseCommand):
    help = "Minimise personal data"

    def handle(self, *args, **options):
        minimised = minimise_data()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully minimised {minimised} objects")
        )
