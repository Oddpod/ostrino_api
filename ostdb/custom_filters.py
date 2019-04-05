from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from ostdb.models import OST, Playlist


def filter_show(queryset, _, value):
    if not value:
        return queryset

    queryset = queryset.filter(show__name__exact=value)
    return queryset


def filter_user(self, queryset, _, value):
    print('the value: ' + value)
    queryset = queryset.filter(created_by=self.request.user)
    return queryset


class OSTFilter(filters.FilterSet):
    filt_title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    show = filters.CharFilter(method=filter_show)

    class Meta:
        model = OST
        fields = ['id', 'filt_title', 'show', 'tags']


class PlaylistFilter(filters.FilterSet):
    isPublic = filters.BooleanFilter(field_name='public')

    class Meta:
        model = Playlist
        fields = '__all__'
