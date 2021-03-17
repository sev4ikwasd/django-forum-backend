from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from authentication.renderers import UserJSONRenderer

from .serializers import UserWithProfileSerializer


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserWithProfileSerializer

    def retrieve(self, request, username=None, *args, **kwargs):
        if username is not None:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user
        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, username=None, *args, **kwargs):
        user_data = request.data.get('user', {})
        if (username is not None) and (username != request.user.username):
            raise PermissionDenied()
        else:
            user = request.user

        serializer = self.serializer_class(user, partial=True, data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
