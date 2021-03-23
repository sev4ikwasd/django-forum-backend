from django.conf.urls import url

from .views import ForumAPIView

app_name = 'forums'

urlpatterns = [
    url('forums', ForumAPIView.as_view()),
]
