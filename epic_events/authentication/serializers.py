from rest_framework import serializers
from authentication.models import User


class UpdatePasswordUserSerializer(serializers.Serializer):
    """
        Serializer for password change endpoint.
    """
    class Meta:
        model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
