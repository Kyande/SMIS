from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from smis.common.permissions import IsAdminOrSystemUser

from .filters import UserFilter
from .models import User
from .serializers import (
    PasswordChangeSerializer, UserDeactivationSerializer,
    UserSerializer, UserLoginSerializer, UserLoginResponseSerializer,
    UserRegistrationSerializer)


class UserViewSet(ModelViewSet):
    """
    User endpoint that handles user related actions

    User actions supported:
        1. User listing.
        2. User Updates.
        3. User Login.
        4. User registration.
        5. User password change.
        6. User account deactivation.
        7. User account reactivation.
        8. User logout.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    ordering = ['-first_name', '-last_name']
    ordering_fields = [
        'first_name', 'last_name', 'date_joined', 'last_login', ]
    # search_fields = ['@first_name', '@last_name']

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
    def login(self, request):
        login_serializer = UserLoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=login_serializer.validated_data['email'],
            password=login_serializer.validated_data['password'],
        )
        if user:
            # user authenticated successfully
            Token.objects.get_or_create(user=user)
            login_resp_serializer = UserLoginResponseSerializer(
                user, context={'request': request})
            return Response(
                login_resp_serializer.data,
                status=status.HTTP_200_OK)

        if not user:
            data = {"error": "User authentication failed"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
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
            data = {"success": "User registration successful"}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception:
            data = {"error": "User registration failed"}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        user = request.user
        # delete user token
        tokens = Token.objects.filter(user=user)
        tokens.delete()
        data = {"success": "User log out successfully"}
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def change_password(self, request):
        user = request.user
        password_reset_serializer = PasswordChangeSerializer(data=request.data)
        password_reset_serializer.is_valid(raise_exception=True)
        authenticated_user = authenticate(
            username=user.email,
            password=password_reset_serializer.validated_data['old_password'],
        )
        if authenticated_user and authenticated_user.is_active:
            user.set_password(
                password_reset_serializer.validated_data['new_password'])
            user.save()
            data = {"success": "Password changed successfully"}
            return Response(data, status=status.HTTP_202_ACCEPTED)

        if not authenticated_user:
            data = {"error": "User credentials provided are not correct"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['POST'], detail=False)
    def deactivate_account(self, request):
        user = request.user
        user_deactivation_serializer = UserDeactivationSerializer(
            data=request.data)
        user_deactivation_serializer.is_valid(raise_exception=True)
        authenticated_user = authenticate(
            username=user.email,
            password=user_deactivation_serializer.validated_data['password'],
        )
        if authenticated_user and authenticated_user.is_active:
            user.is_active = False
            user.save()
            data = {"success": "User account deactivated successfully"}
            return Response(data, status=status.HTTP_202_ACCEPTED)

        if not authenticated_user:
            data = {"error": "User credentials provided are not correct"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

    @action(
        methods=['GET'],
        detail=True,
        permission_classes=[IsAdminOrSystemUser, ])
    def reactivate_account(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        user.is_active = True
        user.save()
        data = {"success": "User account reactivated successfully"}
        return Response(data, status=status.HTTP_202_ACCEPTED)
