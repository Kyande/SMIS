from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import (
    UserSerializer, UserLoginSerializer, UserRegistrationSerializer)


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
        login_serializer = UserLoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        # TODO: Login stuff
        return

    @action(methods=['POST'], detail=False)
    def register(self, request):
        registration_serializer = UserRegistrationSerializer(
            data=request.data)
        registration_serializer.is_valid(raise_exception=True)
        # TODO: Handle exception and return respective HTTP response
        try:
            user = User(**registration_serializer.validated_data)
            user.save()
            return
        except Exception as e:
            return
