from rest_framework import viewsets, status
from rest_framework.views import Response
from rest_framework.decorators import action

from cart.models import Cart
from cart.utils import get_cart, change_product_cart_amount
from api.serializers.cart_serializers import (
    CartSerializer, ProductCartCreateSerializer, ProductCartListSerializer
)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        cart = get_cart(request)
        serializer = self.get_serializer_class()
        context = self.get_serializer_context()
        return Response(
            serializer(
                cart,
                context=context
            ).data,
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        cart = get_cart(request)
        product = int(request.data.get('product'))
        amount = int(request.data.get('amount'))
        serializer = ProductCartCreateSerializer(
            data={
                'cart': cart.pk,
                'product': product,
                'amount': amount
            },
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, *args, **kwargs):
        cart = get_cart(request)
        product = int(request.data.get('product'))
        amount = int(request.data.get('amount'))
        serializer = ProductCartCreateSerializer(
            data={
                'cart': cart.pk,
                'product': product,
                'amount': amount
            },
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_206_PARTIAL_CONTENT
        )

    def delete(self, request, *args, **kwargs):
        cart = get_cart(request)
        cart.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=['POST'], url_path='add', detail=False)
    def increase_cart(self, request):
        """Отдельный эндпоинт для увеличения количества товара на единицу."""
        product = change_product_cart_amount(request)
        context = self.get_serializer_context()
        serializer = ProductCartListSerializer(
            product,
            context=context,
        )
        return Response(
            serializer.data, status=status.HTTP_206_PARTIAL_CONTENT
        )

    @action(methods=['POST'], url_path='subtract', detail=False)
    def decrease_cart(self, request):
        """Отдельный эндпоинт для уменьшения количества товара на единицу."""
        product = change_product_cart_amount(request)
        context = self.get_serializer_context()
        serializer = ProductCartListSerializer(
            product,
            context=context,
        )
        return Response(
            serializer.data, status=status.HTTP_206_PARTIAL_CONTENT
        )
