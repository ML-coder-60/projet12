from rest_framework import serializers
from .models import Client, Contract, Event
from authentication.models import User
import datetime


class UserSerializer(serializers.ModelSerializer):
    """
        Serializer account.
    """
    class Meta:
        model = User
        fields = ['id', 'username']

        read_only_fields = ['id', 'username']


class ContractsSerializer(serializers.ModelSerializer):
    """
        Serializer Contract.
        check date payment_due
    """

    class Meta:
        model = Contract
        fields = [
            'id', 'sales_user', 'client_id', 'signed', 'amount', 'payment_due']

    @staticmethod
    def validate_payment_due(value):
        """
          Check date 'payment due' is after the current date.
        """
        if value <= datetime.datetime.now().date():
            raise serializers.ValidationError(
                {"payment_due": "La date de paiement ne doit pas être inferieur à la date du jour"}
            )
        return value


class ClientsSerializer(serializers.ModelSerializer):
    """
        Serializer Client.
    """
    class Meta:
        model = Client
        fields = [
                     'id', 'name', 'email', 'first_name', 'last_name',
                     'phone', 'mobile', 'confirmed', 'date_created',
                     'date_updated', 'sales_user_id'
                     ]


class EventsSerializer(serializers.ModelSerializer):
    """
        Serializer Event.
        check date
        check status ended
    """

    client = ClientsSerializer

    class Meta:
        model = Event
        fields = [
            'contract_id', 'attendees', 'event_date', 'ended', 'support_user_id',
            'client', 'notes'
                 ]

    @staticmethod
    def validate_event_date(value):
        """
           Check date 'event_date' is after the current date.
        """
        if value <= datetime.datetime.now().date():
            raise serializers.ValidationError(
                 {"event_date": "La date de l' événement ne doit pas être inferieur à la date du jour"}
             )
        return value


class ContractsDetailSerializer(serializers.ModelSerializer):
    """
        Serializer Detail Contract.
    """

    client = ClientsSerializer()

    class Meta:
        model = Contract
        fields = [
            'id', 'sales_user', 'client', 'signed', 'amount', 'payment_due',
            'date_created', 'date_updated',
        ]


class ClientsDetailSerializer(serializers.ModelSerializer):
    """
        Serializer Detail Client.
    """

    sales_user = UserSerializer()
    contracts = ContractsSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'email', 'first_name', 'last_name',
            'phone', 'mobile', 'confirmed', 'date_created',
            'date_updated', 'sales_user', 'contracts'
            ]


class EventsDetailSerializer(serializers.ModelSerializer):
    """
        Serializer Detail Event.
    """

    contract = ContractsDetailSerializer()

    class Meta:
        model = Event
        fields = [
            'contract_id', 'contract', 'attendees', 'event_date', 'ended', 'support_user_id',
            'client', 'notes', 'date_created', 'date_updated'
                 ]
