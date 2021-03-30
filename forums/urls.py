from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ForumViewSet, TopicViewSet, CommentViewSet

app_name = 'forums'

router = DefaultRouter()
router.register(r'forums', ForumViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
