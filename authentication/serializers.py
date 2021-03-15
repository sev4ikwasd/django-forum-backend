from rest_framework import serializers

from django.contrib.auth import authenticate 

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password',]
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
