from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'avatar', 'email', 'first_name', 'last_name',
            'date_joined', 'last_login', 'user_type',
            'is_active']
