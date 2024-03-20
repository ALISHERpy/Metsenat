from django_filters import rest_framework as filters
from datetime import datetime

from sponsor.models import Sponsor


class CreatedAtFilter(filters.FilterSet):
    created_at__gt = filters.DateTimeFilter(field_name='created_at', lookup_expr='gt',
                                             label=('Created After'), help_text=('Filter sponsors created after a certain date'))
    created_at__lt = filters.DateTimeFilter(field_name='created_at', lookup_expr='lt',
                                             label=('Created Before'), help_text=('Filter sponsors created before a certain date'))

    class Meta:
        model = Sponsor
        fields = ['balance', 'status','created_at',]
