from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Кастомный пермишен для доступка к объектам.

    Создание, удаление и изменние объектов дотсупно
    только администратору.
    """

    message = 'Доступно только администратору'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
