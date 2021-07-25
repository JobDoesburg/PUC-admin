from django.core.management import BaseCommand

import competitions.management.commands.minimisecompetitionsdata
import questions.management.commands.minimisequestionsdata


def minimise_data():
    minimised = questions.management.commands.minimisequestionsdata.minimise_data()
    minimised += (
        competitions.management.commands.minimisecompetitionsdata.minimise_data()
    )
    return minimised


class Command(BaseCommand):
    help = "Minimise personal data"

    def handle(self, *args, **options):
        minimised = minimise_data()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully minimised {minimised} objects")
        )
