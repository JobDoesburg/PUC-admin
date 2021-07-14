from import_export import resources

from .models import School


class SchoolResource(resources.ModelResource):
    class Meta:
        model = School
        exclude = ()
