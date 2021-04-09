from rest_framework import serializers

from authentication.models import User
from .models import Forum, Topic, Comment

class ForumSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = ('title', 'slug', 'topics',)
        read_only_fields = ('slug', 'topics',)

# Get 5 latest created topic names
    def get_topics(self, obj):
        slice_size = Topic.objects.filter(forum=obj).count()
        slice_size = 5 if slice_size > 5 else slice_size
        sliced_topics = Topic.objects.filter(forum=obj).order_by('created_time').reverse()[:slice_size]
        return reversed(list(map(lambda topic: topic.title, sliced_topics)))

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
