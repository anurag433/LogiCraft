import django_filters
from .models import Driver

class DriverFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=Driver.Status.choices
    )
    experience_min = django_filters.NumberFilter(
        field_name="experience_years",
        lookup_expr="gte"
    )
    experience_max = django_filters.NumberFilter(
        field_name="experience_years",
        lookup_expr="lte"
    )
    class Meta:
        model = Driver
        fields = [
            "status",
            "experience_min",
            "experience_max",
        ]