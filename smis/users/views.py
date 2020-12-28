from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer


class UserView(ModelViewSet):
    """
    A View to handle everything user related.

    Things to consider:
    1. login.
    2. registration.
    3. User listing.
    4. User deactivation.
    5. Password change.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        return

    @action(methods=['POST'], detail=False)
    def register(self, request):
        return
