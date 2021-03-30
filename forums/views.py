from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Forum, Topic, Comment
from .serializers import ForumSerializer, TopicSerializer, CommentSerializer
from .filters import TopicFilter, CommentFilter

class ForumViewSet(mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Forum.objects.all()
    search_fields = ('title',)
    serializer_class = ForumSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if (self.action == 'create') or (self.action == 'destroy'):
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)
        return (permission() for permission in permission_classes)

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    search_fields = ('title',)
    serializer_class = TopicSerializer
    lookup_field = 'slug'
    filterset_class = TopicFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer_data['author'] = request.user

        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, slug, *args, **kwargs):
        instance = get_object_or_404(Topic, slug=slug)
        if (instance.creator != request.user) or (request.data.get('forum', None) != None):
            raise PermissionDenied()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    search_field = ('text',)
    serializer_class = CommentSerializer
    lookup_field = 'id'
    filterset_class = CommentFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer_data['author'] = request.user

        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, id, *args, **kwargs):
        instance = get_object_or_404(Comment, id=id)
        if (instance.author != request.user) or (request.data.get('topic', None) != None):
            raise PermissionDenied()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    