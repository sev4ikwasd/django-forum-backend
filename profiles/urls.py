from django.conf.urls import url
from django.urls import path

from .views import ProfileAPIView, OtherProfileAPIView

app_name = 'profiles'

urlpatterns = [
    path('profiles/<str:username>', OtherProfileAPIView.as_view()),
    url('profile', ProfileAPIView.as_view()),
]
