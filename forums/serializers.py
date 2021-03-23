from rest_framework import serializers

from .models import Forum, Topic

class TopicNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('title', 'slug',)
        read_only_fields = ('title', 'slug',)

class ForumSerializer(serializers.ModelSerializer):
    topics = TopicNameSerializer(many=True)

    class Meta:
        model = Forum
        fields = ('title', 'topics',)
        read_only_fields = ('title', 'topics',)
