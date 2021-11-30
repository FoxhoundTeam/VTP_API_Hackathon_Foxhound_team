from django_filters.rest_framework import FilterSet, DateFilter

class ViolationFilterSet(FilterSet):
    dt_from = DateFilter(field_name='dttm', lookup_expr='date__gte')
    dt_to = DateFilter(field_name='dttm', lookup_expr='date__lte')