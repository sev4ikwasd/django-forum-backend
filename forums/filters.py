from django_filters.rest_framework import FilterSet
from django_filters import CharFilter, NumberFilter

from .models import Topic, Comment

class TopicFilter(FilterSet):
    title = CharFilter(field_name='title')
    forum = CharFilter(field_name='forum__slug')
    creator = CharFilter(field_name='creator__username')

    class Meta:
        model = Topic
        fields = ['title', 'forum', 'creator',]

class CommentFilter(FilterSet):
    id = NumberFilter(field_name='id')
    topic = CharFilter(field_name='topic__slug')
    author = CharFilter(field_name='author__username')

    class Meta:
        model = Comment
        fields = ['id', 'topic', 'author',] 
