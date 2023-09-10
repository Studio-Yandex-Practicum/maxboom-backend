from rest_framework import permissions

ALLOWED_METHOD = ('POST', 'GET', 'HEAD', 'OPTIONS')


class IsAdminOrAnyUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.method in ALLOWED_METHOD
