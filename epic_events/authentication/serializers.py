from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    """
        Serializer for create account endpoint.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdatePasswordUserSerializer(serializers.Serializer):
    """
        Serializer for password change endpoint.
    """
    class Meta:
        model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
