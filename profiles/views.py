from django.shortcuts import render, get_object_or_404

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User

from .serializers import UserWithProfileSerializer

class ProfileAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserWithProfileSerializer

    def retrieve(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
