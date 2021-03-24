from rest_framework import serializers

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
