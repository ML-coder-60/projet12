from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from .permissions import ClientPermission
from .models import Client
from .serializers import (
    ClientsSerializer,
    ClientsDetailSerializer
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
        The potential client are managed by users with the sales role:
             Methode: LIST/DETAIL/PUT/POST
        The client are managed by users with the sales role :
            Methode: LIST/DETAIL/PUT
        The client are listed by user with the support role
            Methode: LIST/DETAIL
    """

    serializer_class = ClientsSerializer
    detail_serializer_class = ClientsDetailSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^first_name', '^last_name', '^email', '^name']
    filterset_fields = ['confirmed', 'sales_user']

    http_method_names = ['get', 'post', 'head', 'put', 'delete']

    permission_classes = [IsAuthenticated, ClientPermission]

    def get_queryset(self):
        """
            return all projects whitch user authenticated
            Team Sales : view all clients
            Team Support : view clients confirmed
        """
        if self.request.user.team == 'Support':
            clients = Client.objects.exclude(confirmed=False)
        elif self.request.user.team == 'Commercial' or self.request.user.team == 'Gestion':
            clients = Client.objects.all()
        else:
            clients = None
        if clients.count() >= 1:
            return clients
        else:
            get_object_or_404(clients)

    def create(self, request, *args, **kwargs):
        """
        Request method : POST
        Only sales member could create a new client.
            If serializer company is OK :
                creation of a Company object whih sales_user_id = id user.

            :return: serializer.data or serializer.error
        """
        data = request.data.copy()
        data['sales_user'] = self.request.user.id
        serializer = ClientsDetailSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
