from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
# from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .permissions import ClientPermission, ContractPermission, EventPermission
from .models import Client, Contract, Event
from .serializers import (
    ClientsSerializer,
    ClientsDetailSerializer,
    ContractsSerializer,
    ContractsDetailSerializer,
    EventsSerializer,
    EventsDetailSerializer
)


class MultipleSerializerMixin:
    """
        Set serializer
    """

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ClientsViewset(MultipleSerializerMixin, ModelViewSet):
    """
        Endpoint manage Clients
    """

    serializer_class = ClientsSerializer
    detail_serializer_class = ClientsDetailSerializer

    # filter_backends = [SearchFilter, DjangoFilterBackend]
    # search_fields = ['^first_name', '^last_name', '^email', '^name']
    # filterset_fields = ['confirmed', 'sales_user_id']

    http_method_names = ['get', 'post', 'head', 'put']

    permission_classes = [IsAuthenticated, ClientPermission]

    def get_queryset(self):
        """
            return all projects whitch user authenticated
            Team Sales : view all clients
            Team Support : view clients confirmed
        """
        if self.request.user.team == 'Support':
            clients = Client.objects.exclude(confirmed=False)
        elif self.request.user.team == 'Commercial':
            clients = Client.objects.all()
        else:
            clients = None
        if clients.count() >= 1:
            return clients
        else:
            get_object_or_404(clients)

    def perform_create(self, serializer):
        """
        Request method : POST
        Only sales member could create a new client.
            If serializer company is OK :
                creation of a Company object whih sales_user_id = id user.

            :return: serializer.data or serializer.error
        """
        serializer.save(sales_user=self.request.user)


class ContractsViewset(MultipleSerializerMixin, ModelViewSet):
    """
        Endpoint manage Contracts
    """

    serializer_class = ContractsSerializer
    detail_serializer_class = ContractsDetailSerializer

    # filter_backends = [SearchFilter, DjangoFilterBackend]
    # search_fields = ['^contract', ]
    # filterset_fields = ['signed', ]

    http_method_names = ['get', 'post', 'head', 'put']

    permission_classes = [IsAuthenticated, ContractPermission]

    def get_queryset(self):
        """
            return all Contracts whitch user authenticated
        """
        contracts = Contract.objects.all()
        if contracts.count() >= 1:
            return contracts
        else:
            get_object_or_404(contracts)

    def create(self, request, *args, **kwargs):
        """
               Request method : POST
                  Only sales member and owner create a new contract.
                  before create contract check:
                      client exist and
                      Client confirmed

                  creation contract
                      if contracts is signed:
                          creation events
        """

        client = Client.objects.filter(Q(id=self.request.data['client_id']) & Q(confirmed=True))

        if client.count() != 1:
            return Response(
                {
                    'detail': f"Pas de client 'confirmé' avec client_id: {self.request.data['client_id']}"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        data = serializer.save(client_id=self.request.data['client_id'])
        if data.signed:
            Event.objects.get_or_create(contract_id=data.id)

    def update(self, request, *args, **kwargs):
        """
             Request method : PUT
                Only sales member and owner Update contract.
                before update contract Check
                    client exist and
                    client confirmed
                    contract exist
                    contact not signed
                update contracts:
                    if contracts is signed:
                        creation events
        """

        client = Client.objects.filter(Q(id=self.request.data['client_id']) & Q(confirmed=True))
        if client.count() != 1:
            return Response(
                {'detail': f"Pas de client 'confirmé' avec client_id: {self.request.data['client_id']}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance = self.get_object()
        if instance.signed:
            return Response(
                {'detail': 'Le contrat est signé par le client modification impossible'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        data = serializer.save(client_id=self.request.data['client_id'])
        if data.signed:
            Event.objects.get_or_create(contract_id=data.id)


class EventsViewset(MultipleSerializerMixin, ModelViewSet):
    """
        Endpoint manage events
    """
    serializer_class = EventsSerializer
    detail_serializer_class = EventsDetailSerializer

    # filter_backends = [SearchFilter, DjangoFilterBackend]
    # search_fields = ['^event_date', ]
    # filterset_fields = ['ended', ]

    http_method_names = ['get', 'head', 'put']

    permission_classes = [IsAuthenticated, EventPermission]


    def get_queryset(self):
        """
            return all Events with support_id
        """
        events = Event.objects.exclude(support_user=None)
        if events.count() >= 1:
            return events
        else:
            get_object_or_404(events)

    queryset = Event.objects.all()

    def update(self, request, *args, **kwargs):
        """
              Request method : PUT
                 Only
                     sales member and owner  or
                     support menber and responsable of event.
        """

        instance = self.get_object()
        if instance.ended:
            return Response(
               {'ended': f"L'événement : {instance.contract_id} est fermé modification impossible"},
               status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()
