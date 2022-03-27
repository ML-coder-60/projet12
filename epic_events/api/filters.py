import django_filters
from .models import Client, Contract, Event


class ClientFilterSet(django_filters.FilterSet):
    sales_user_username = django_filters.CharFilter(field_name='sales_user_id__username')

    class Meta:
        model = Client
        fields = ['sales_user_username', 'sales_user_id', 'confirmed']


class ContractFilterSet(django_filters.FilterSet):
    client_name = django_filters.CharFilter(field_name='client_id__name')
    sales_user_id = django_filters.CharFilter(field_name='client_id__sales_user__id')
    sales_user_username = django_filters.CharFilter(field_name='client_id__sales_user__username')

    class Meta:
        model = Contract
        fields = [
            'signed', 'id', 'client_id', 'client_name', 'sales_user_id',
            'sales_user_username', 'amount', 'payment_due'
        ]


class EventFilterSet(django_filters.FilterSet):
    client_name = django_filters.CharFilter(field_name='contract__client__name')
    client_id = django_filters.CharFilter(field_name='contract__client__id')
    support_user_id = django_filters.CharFilter(field_name='support_user_id')
    support_user_username = django_filters.CharFilter(field_name='support_user__username')
    contract_id = django_filters.CharFilter(field_name='contract__id')

    class Meta:
        model = Event
        fields = [
            'event_date', 'attendees', 'support_user_id', 'support_user_username', 'client_name',
            'contract_id', 'ended', 'client_id', 'notes'
        ]
