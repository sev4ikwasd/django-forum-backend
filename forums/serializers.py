from rest_framework import serializers

from authentication.models import User
from .models import Forum, Topic

class TopicNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('title', 'slug',)

class ForumSerializer(serializers.ModelSerializer):
    topics = TopicNameSerializer(many=True, read_only=True)

    class Meta:
        model = Forum
        fields = ('title', 'slug', 'topics',)
        read_only_fields = ('slug', 'topics',)

class TopicSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    forum = serializers.SlugRelatedField(slug_field='slug', queryset=Forum.objects.all())

    class Meta:
        model = Topic
        fields = ('title', 'slug', 'creator', 'forum', 'created_time', 'changed_time')
        read_only_fields = ('slug', 'created_time', 'changed_time')