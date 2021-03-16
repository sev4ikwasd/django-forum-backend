from django.core.exceptions import ValidationError

from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from authentication.models import User

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Profile
        exclude = ('id', 'user',)
    
    def get_image(self, obj):
        if obj.image:
            return obj.image

        #TODO default image
        return None

class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile',]

    def validate_image(self, obj):
        if obj.file.size > (2*1024*1024):
            raise ValidationError('Max file size is 2Mib.')

    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        profile = validated_data.pop('profile', None)

        if username is not None:
            setattr(instance, 'username', username)
        
        if profile is not None:
            for (key, value) in profile.items():
                setattr(instance.profile, key, value)

        instance.profile.save()
        instance.save()

        return instance