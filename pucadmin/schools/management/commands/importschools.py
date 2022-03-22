import csv

import requests
from django.core.management import BaseCommand

from organisations.models import Course
from schools.models import School


def import_schools():
    url = "https://duo.nl/open_onderwijsdata/images/02-alle-vestigingen-vo.csv"
    with requests.Session() as s:
        download = s.get(url)
    decoded_content = download.content.decode("unicode_escape")
    schools = csv.DictReader(decoded_content.splitlines(), delimiter=";")
    num_created = 0
    dissolved_before = School.objects.filter(dissolved=True).count()
    School.objects.all().update(dissolved=True)
    for school in schools:
        if "VWO" in school["ONDERWIJSSTRUCTUUR"]:
            update_values = {
                "name": school["VESTIGINGSNAAM"],
                "location_street": school["STRAATNAAM"],
                "location_house_number": school["HUISNUMMER-TOEVOEGING"],
                "location_zip": school["POSTCODE"],
                "location_town": school["PLAATSNAAM"],
                "correspondence_street": school["STRAATNAAM CORRESPONDENTIEADRES"],
                "correspondence_house_number": school[
                    "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES"
                ],
                "correspondence_zip": school["POSTCODE CORRESPONDENTIEADRES"],
                "correspondence_town": school["PLAATSNAAM CORRESPONDENTIEADRES"],
                "phone": school["TELEFOONNUMMER"],
                "url": school["INTERNETADRES"],
                "dissolved": False,
            }
            _, created = School.objects.update_or_create(
                bg_id=school["BEVOEGD GEZAG NUMMER"],
                brin_id=school["BRIN NUMMER"],
                location_id=school["VESTIGINGSNUMMER"],
                defaults=update_values,
            )
            if created:
                num_created += 1
    dissolved_after = School.objects.filter(dissolved=True).count()
    import_courses()
    return num_created, max(dissolved_after - dissolved_before, 0)


def import_courses():
    url = "https://duo.nl/open_onderwijsdata/images/10-examenkandidaten-vwo-en-examencijfers-2020-2021.csv"
    with requests.Session() as s:
        download = s.get(url)
    decoded_content = download.content.decode("unicode_escape")
    courses = csv.DictReader(decoded_content.splitlines(), delimiter=";")
    for c in courses:
        try:
            school = School.objects.get(
                brin_id=c["BRIN NUMMER"],
                location_id=c["BRIN NUMMER"] + c["VESTIGINGSNUMMER"],
            )
        except School.DoesNotExist:
            continue

        try:
            course = Course.objects.get(gov_slug=c["AFKORTING VAKNAAM"])
        except Course.DoesNotExist:
            continue

        school.courses_offered.add(course)


class Command(BaseCommand):
    help = "Imports schools from DUO."

    def handle(self, *args, **options):
        num_created, num_dissolved = import_schools()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {num_created} new schools, {num_dissolved} schools have been dissolved."
            )
        )
