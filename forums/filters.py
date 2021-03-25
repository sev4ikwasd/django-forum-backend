from django_filters.rest_framework import FilterSet
from django_filters import CharFilter

from .models import Topic

class TopicFilter(FilterSet):
    title = CharFilter(field_name='title')
    forum = CharFilter(field_name='forum__slug')
    creator = CharFilter(field_name='creator__username')

    class Meta:
        model = Topic
        fields = ['title', 'forum', 'creator',]