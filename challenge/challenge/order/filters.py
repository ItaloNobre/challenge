from django_filters import rest_framework as filters

from challenge.order.models import Order


class OrderFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name='is_active')
    code = filters.CharFilter(field_name='code')
    title = filters.CharFilter(field_name='title')

    class Meta:
        model = Order
        fields = {}
