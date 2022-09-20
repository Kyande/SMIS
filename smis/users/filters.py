from django_filters import rest_framework as filters

from .models import User


class UserFilter(filters.FilterSet):
    date_joined = filters.IsoDateTimeFromToRangeFilter()
    last_login = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = User
        fields = ('date_joined', 'last_login', 'user_type', 'is_active', )
