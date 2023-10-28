from rest_framework import viewsets, views
from rest_framework.views import Response

from cart.models import Cart
from api.serializers.cart_serializers import CartSerializer
from api.permissions.cart_permissions import CartPermission


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [CartPermission, ]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
