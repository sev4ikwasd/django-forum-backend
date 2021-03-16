from django.shortcuts import render, get_object_or_404

from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from authentication.renderers import UserJSONRenderer

from .serializers import UserWithProfileSerializer


class OtherProfileAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserWithProfileSerializer

    def retrieve(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserWithProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        serializer = self.serializer_class(request.user, partial=True, data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
