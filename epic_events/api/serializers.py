from rest_framework import serializers
from .models import Client
from authentication.serializers import User


class ClientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'email', 'first_name', 'last_name',
            'confirmed', 'phone', 'mobile', 'sales_user'
            ]


class ClientsDetailSerializer(serializers.ModelSerializer):

    sales_user_id = User

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'email', 'first_name', 'last_name',
            'phone', 'mobile', 'confirmed', 'date_created',
            'date_updated', 'sales_user'
            ]
