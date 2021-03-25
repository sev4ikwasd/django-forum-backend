from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ForumViewSet, TopicViewSet

app_name = 'forums'

router = DefaultRouter()
router.register(r'forums', ForumViewSet)
router.register(r'topics', TopicViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
