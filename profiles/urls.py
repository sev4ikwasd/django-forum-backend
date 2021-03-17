from django.conf.urls import url
from django.urls import path

from .views import ProfileAPIView

app_name = 'profiles'

urlpatterns = [
    url(r'^profiles(?:/(?P<username>.+))?/$', ProfileAPIView.as_view())
]
