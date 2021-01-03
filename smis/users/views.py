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
            login_resp_serializer = UserLoginResponseSerializer(
                user, context={'request': request})
            return Response(
                login_resp_serializer.data,
                status=status.HTTP_200_OK)
        else:
            data = {"user": "User authentication failed"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def register(self, request):
        registration_serializer = UserRegistrationSerializer(
            data=request.data)
        registration_serializer.is_valid(raise_exception=True)
        try:
            validated_data = {**registration_serializer.validated_data}
            # remove repeated password entry
            validated_data.pop('repeat_password')
            # remove password entry
            password = validated_data.pop('password')
            user = User(**validated_data)
            # set user password
            user.set_password(password)
            user.save()
            data = {"user": "User registration successful"}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception:
            data = {"user": "User registration failed"}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        user = request.user
        # delete user token
        tokens = Token.objects.filter(user=user)
        tokens.delete()
        data = {"user": "User log out successfully"}
        return Response(data, status=status.HTTP_200_ACCEPTED)
