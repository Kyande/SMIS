from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import (
    UserSerializer, UserLoginSerializer,
    UserLoginResponseSerializer, UserRegistrationSerializer)


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
        user = authenticate(
            username=login_serializer.validated_data['email'],
            password=login_serializer.validated_data['password']
        )
        if user:
            # user authenticated successfully
            Token.objects.get_or_create(user=user)
            return Response(
                UserLoginResponseSerializer(user).data,
                status=status.HTTP_200_OK)
        else:
            data = {"user": "User authentication failed"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

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
