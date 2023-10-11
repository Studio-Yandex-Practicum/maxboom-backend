from rest_framework import permissions


class IsAdminOrPostOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_staff
        else:
            return True
