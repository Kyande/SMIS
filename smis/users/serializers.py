from rest_framework import serializers

from .models import User, USER_TYPES


class UserSerializer(serializers.HyperlinkedModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

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
        max_length=10, write_only=True, allow_null=False, required=True,
        trim_whitespace=True)


class UserRegistrationSerializer(serializers.Serializer):
    avatar = serializers.ImageField(
        write_only=True, required=False, allow_null=True)
    email = serializers.EmailField(
        write_only=True, required=True, allow_null=False)
    first_name = serializers.CharField(
        max_length=50, write_only=True, required=True, allow_null=False,
        trim_whitespace=True)
    last_name = serializers.CharField(
        max_length=50, write_only=True, required=True, allow_null=False,
        trim_whitespace=True)
    user_type = serializers.ChoiceField(
        write_only=True, choices=USER_TYPES, required=True,
        allow_null=False)
    password = serializers.CharField(
        max_length=10, write_only=True, allow_null=False, required=True,
        trim_whitespace=True)
    repeat_password = serializers.CharField(
        min_length=8, max_length=10, write_only=True, allow_null=False,
        required=True, trim_whitespace=True)

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)
        if self.password != self.repeat_password:
            raise serializers.ValidationError({"password": "your passwords do not match"})
