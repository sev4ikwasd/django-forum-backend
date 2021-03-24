from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ForumViewSet

app_name = 'forums'

router = DefaultRouter()
router.register(r'forums', ForumViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
