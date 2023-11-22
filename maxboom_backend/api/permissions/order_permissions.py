from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.is_authenticated:
            return obj.user == request.user
        return obj.session_id == request.session.get('anonymous_id')


class IsOwnerOrAdminRefund(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.is_authenticated:
            return obj.order.user == request.user
        return obj.order.session_id == request.session.get('anonymous_id')


class IsOwnerOrAdminPayment(IsOwnerOrAdminRefund):
    pass


class IsOwnerOrAdminRepayment(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.is_authenticated:
            return obj.order.user == request.user
        return obj.order.session_id == request.session.get('anonymous_id')
