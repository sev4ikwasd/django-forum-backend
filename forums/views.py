from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Forum
from .serializers import ForumSerializer

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

