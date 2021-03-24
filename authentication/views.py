from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from .serializers import RegistrationSerializer

class RegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
