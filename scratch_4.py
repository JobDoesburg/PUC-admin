import csv

from schools.models import School

adr_file = open("../adreslabels.csv", "r")
addresses = list(csv.DictReader(adr_file, delimiter=","))
schools = School.objects.all()


def match_school(adr):
    for school in schools:
        if school.location_zip == adr["postcode"]:
            return school
        if school.correspondence_zip == adr["postcode"]:
            return school
    return None


match = {}
no_match = []
for adr in addresses:
    if (
        adr["school"]
        and adr["school"] not in no_match
        and adr["school"] not in match.keys()
    ):
        school = match_school(adr)
        if school:
            school.short_name = adr["school"]
            school.save()
            print(f"{adr['school']} == {school}")
            match[adr["school"]] = school
        else:
            print(f"No match for {adr['school']}")
            no_match.append(adr["school"])
