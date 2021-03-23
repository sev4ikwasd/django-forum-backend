from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter

from .models import Forum
from .serializers import ForumSerializer

class ForumAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Forum.objects.all()
    search_fields = ('title',)
    serializer_class = ForumSerializer
