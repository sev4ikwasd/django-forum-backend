from rest_framework import serializers

from authentication.models import User
from .models import Forum, Topic, Comment

#Get 5 latest created topics
def _get_topic_queryset():
    slice_size = Topic.objects.count()
    if slice_size > 5:
        slice_size = 5
    return Topic.objects.order_by('created_time')[:slice_size]

class TopicNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('title', 'slug',)

class ForumSerializer(serializers.ModelSerializer):
    topics = TopicNameSerializer(_get_topic_queryset(), many=True, read_only=True)

    class Meta:
        model = Forum
        fields = ('title', 'slug', 'topics',)
        read_only_fields = ('slug', 'topics',)

class TopicSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    forum = serializers.SlugRelatedField(slug_field='slug', queryset=Forum.objects.all())

    class Meta:
        model = Topic
        fields = ('title', 'slug', 'creator', 'forum', 'created_time', 'changed_time')
        read_only_fields = ('slug', 'created_time', 'changed_time',)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    topic = serializers.SlugRelatedField(slug_field='slug', queryset=Topic.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'topic', 'written_time', 'changed_time',)
        read_only_fields = ('id', 'written_time', 'changed_time',)
