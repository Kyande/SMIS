from rest_framework import serializers

from .models import User, USER_TYPES


class UserSerializer(serializers.HyperlinkedModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'url', 'id', 'avatar', 'email',
            'first_name', 'last_name', 'date_joined',
            'last_login', 'user_type', 'is_active']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True, required=True, allow_null=False)
    password = serializers.CharField(
        min_length=8, max_length=10, write_only=True, allow_null=False,
        required=True, trim_whitespace=True)


class UserLoginResponseSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token')
    id = serializers.UUIDField(format='hex_verbose')

    class Meta:
        model = User
        fields = [
            'token', 'id', 'avatar', 'first_name', 'last_name',
            'email', 'date_joined', 'last_login', 'user_type',
            'is_active'
        ]
        read_only_fields = fields


class UserRegistrationSerializer(serializers.Serializer):
    avatar = serializers.ImageField(
        write_only=True, required=False, allow_null=True)
    email = serializers.EmailField(
        write_only=True, required=True, allow_null=False)
    first_name = serializers.CharField(
        max_length=50, write_only=True, required=True,
        allow_null=False, trim_whitespace=True)
    last_name = serializers.CharField(
        max_length=50, write_only=True, required=True,
        allow_null=False, trim_whitespace=True)
    user_type = serializers.ChoiceField(
        write_only=True, choices=USER_TYPES, required=True,
        allow_null=False)
    password = serializers.CharField(
        min_length=8, max_length=10, write_only=True,
        allow_null=False, required=True, trim_whitespace=True)
    repeat_password = serializers.CharField(
        min_length=8, max_length=10, write_only=True,
        allow_null=False, required=True, trim_whitespace=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"})
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        min_length=8, max_length=10, write_only=True,
        allow_null=False, required=True, trim_whitespace=True)
    new_password = serializers.CharField(
        min_length=8, max_length=10, write_only=True,
        allow_null=False, required=True, trim_whitespace=True)
    repeat_new_password = serializers.CharField(
        min_length=8, max_length=10, write_only=True,
        allow_null=False, required=True, trim_whitespace=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                {"password": "New password should not match old password"})

        if attrs['new_password'] != attrs['repeat_new_password']:
            raise serializers.ValidationError(
                {"password": "New passwords do not match"})
        return attrs


class UserDeactivationSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, max_length=10, write_only=True,
        allow_null=False, required=True, trim_whitespace=True)
