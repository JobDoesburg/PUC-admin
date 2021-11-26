from django.core.management import BaseCommand
from django.utils import timezone

from questions.models import Student


def minimise_data():
    deleted, _ = Student.objects.filter(
        question__created_at__lt=timezone.now() - timezone.timedelta(days=365),
    ).delete()
    return deleted


class Command(BaseCommand):
    help = "Deletes personal information from students."

    def handle(self, *args, **options):
        deleted = minimise_data()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully minimised {deleted} objects")
        )
