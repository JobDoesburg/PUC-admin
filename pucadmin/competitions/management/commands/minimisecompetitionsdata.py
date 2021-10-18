from django.core.management import BaseCommand
from django.utils import timezone

from competitions.models import Student, Supervisor


def minimise_data():
    empty_data_student = {
        "address_1": None,
        "address_2": None,
        "zip": None,
        "town": None,
        "email": None,
        "phone": None,
    }
    empty_data_supervisor = {
        "email": None,
        "phone": None,
    }
    updated = Student.objects.filter(
        submission__competition__competition_date__lt=timezone.now()
        - timezone.timedelta(days=31)
    ).update(**empty_data_student)
    updated += Supervisor.objects.filter(
        submission__competition__competition_date__lt=timezone.now()
        - timezone.timedelta(days=31)
    ).update(**empty_data_supervisor)
    return updated


class Command(BaseCommand):
    help = "Deletes personal information from students and supervisors."

    def handle(self, *args, **options):
        deleted = minimise_data()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully minimised {deleted} objects")
        )
