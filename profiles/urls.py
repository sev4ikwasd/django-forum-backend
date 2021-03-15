from django.urls import path

from .views import ProfileAPIView

app_name = 'profiles'

urlpatterns = [
    path('profiles/<str:username>', ProfileAPIView.as_view()),
]
