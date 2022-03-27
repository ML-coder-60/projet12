from rest_framework import serializers
from .models import Client, Contract, Event
import datetime


class ContractsSerializer(serializers.ModelSerializer):
    """
        Serializer Contract.
        check date payment_due
    """

    class Meta:
        model = Contract
        fields = [
            'id', 'sales_user_id', 'sales_user_username', 'client_id',
            'client_name', 'signed', 'amount', 'payment_due'
        ]

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
                    'phone', 'mobile', 'confirmed', 'sales_user_id',
                    'sales_user_username'
                     ]


class ClientsDetailSerializer(serializers.ModelSerializer):
    """
        Serializer Detail Client.
    """

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'email', 'first_name', 'last_name',
            'phone', 'mobile', 'confirmed', 'date_created',
            'date_updated', 'sales_user_id', 'sales_user_username'
            ]


class EventsSerializer(serializers.ModelSerializer):
    """
        Serializer Event.
        check date
    """

    client = ClientsSerializer

    class Meta:
        model = Event
        fields = [
            'contract_id', 'attendees', 'event_date', 'ended', 'support_user_id', 'support_user_username',
            'client_id', 'client_name'
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
            'id', 'sales_user_id', 'sales_user_username', 'client', 'signed', 'amount', 'payment_due',
            'date_created', 'date_updated',
        ]


class EventsDetailSerializer(serializers.ModelSerializer):
    """
        Serializer Detail Event.
    """

    contract = ContractsDetailSerializer()

    class Meta:
        model = Event
        fields = [
            'attendees', 'event_date', 'ended', 'support_user_id', 'support_user_username',
            'notes', 'date_created', 'date_updated', 'contract'
                 ]
