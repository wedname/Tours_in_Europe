import django_filters
from .models import ToursInEurope


class ToursFilter(django_filters.FilterSet):

    class Meta:
        model = ToursInEurope
        fields = ["country"]
