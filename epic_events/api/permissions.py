from rest_framework import permissions


class ClientPermission(permissions.BasePermission):
    """
        method authorised : 'GET', 'OPTIONS' and 'HEAD'
        other method authorized:  for customer's business
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if 'Commercial' == request.user.team or 'Gestion' == request.user.team:
            return True

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.sales_user_id
