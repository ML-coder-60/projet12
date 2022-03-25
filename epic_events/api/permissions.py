from rest_framework import permissions
from django.db.models import Q
from api.models import Client, Contract


class ClientPermission(permissions.BasePermission):
    """
        method authorised : 'GET', 'OPTIONS' and 'HEAD'
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if 'Commercial' == request.user.team:
            return True

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.sales_user.id


class ContractPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # check user team sales and owner client
        if 'Commercial' == request.user.team and 'client_id' in request.data:
            if Client.objects.filter(
                    Q(id=request.data['client_id']) &
                    Q(sales_user_id=request.user.id)
                    ).exists():
                return True


class EventPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if 'Commercial' == request.user.team or 'Support' == request.user.team:
            return True

    def has_object_permission(self, request, view, obj):
        client_id = Contract.objects.get(pk=view.kwargs['pk']).client_id
        if Client.objects.filter(
                Q(id=client_id) &
                Q(sales_user_id=request.user.id)
                ).exists():
            return True
        return request.user.id == obj.support_user.id
