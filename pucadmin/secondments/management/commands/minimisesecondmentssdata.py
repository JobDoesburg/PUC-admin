from django.core.management import BaseCommand
from django.utils import timezone

from secondments.models import Employee


def minimise_data():
    deleted, _ = Employee.objects.filter(
        timeperiod__end__lt=timezone.now() - timezone.timedelta(days=365),
    ).delete()
    return deleted


class Command(BaseCommand):
    help = "Deletes personal information from secondment employees."

    def handle(self, *args, **options):
        deleted = minimise_data()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully minimised {deleted} objects")
        )
