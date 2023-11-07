from rest_framework import viewsets, status, mixins
from rest_framework.views import Response
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
)

from cart.models import Cart
from cart.utils import (
    get_cart, change_product_cart_amount,
    list_cart_product, process_cart_product
)
from api.serializers.cart_serializers import (
    CartSerializer, ProductCartCreateSerializer,
    ProductCartListSerializer, ProductCartChangeSerializer
)


@extend_schema(
    tags=["Корзина"],
    summary="Корзина",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получение корзины",
        description="""Получение корзины текущего
        пользователя или сессии. Корзина неавторизованной
        сессии при авторизации переносится в аккаунт.
        """,
        responses={status.HTTP_200_OK: CartSerializer}
    ),
    create=extend_schema(
        summary="Добавление в корзину",
        description="""Добавление товара в корзину. Для
        успешного запроса нужно предоставить id корзины,
        id товара и его количество.
        """,
        request=ProductCartCreateSerializer,
        responses={status.HTTP_201_CREATED: ProductCartCreateSerializer},
    ),
    update=extend_schema(
        summary="Обновление количества продукта в корзине",
        request=ProductCartCreateSerializer,
        responses={status.HTTP_201_CREATED: ProductCartCreateSerializer},
    ),
    destroy=extend_schema(
        summary="Очистка корзины",
    )
)
class CartViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet
                  ):
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = None
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

    def create(self, request, *args, **kwargs):
        return process_cart_product(
            request,
            context=self.get_serializer_context(),
        )

    def put(self, request, *args, **kwargs):
        return process_cart_product(
            request,
            context=self.get_serializer_context(),
        )

    def delete(self, request, *args, **kwargs):
        cart = get_cart(request)
        cart.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        summary="Увеличение количества товара",
        request=ProductCartChangeSerializer,
        responses={status.HTTP_206_PARTIAL_CONTENT: ProductCartListSerializer},
    )
    @action(methods=['PUT'], url_path='add', detail=False)
    def increase_product_cart(self, request):
        """Отдельный эндпоинт для увеличения количества товара на единицу."""
        product = change_product_cart_amount(request)
        context = self.get_serializer_context()
        return list_cart_product(product, context)

    @extend_schema(
        summary="Уменьшение количества товара",
        request=ProductCartChangeSerializer,
        responses={
            status.HTTP_206_PARTIAL_CONTENT: ProductCartListSerializer,
            status.HTTP_204_NO_CONTENT: None
        },
    )
    @action(methods=['PUT'], url_path='subtract', detail=False)
    def decrease_product_cart(self, request):
        """Отдельный эндпоинт для уменьшения количества товара на единицу."""
        product = change_product_cart_amount(request)
        context = self.get_serializer_context()
        return list_cart_product(product, context)

    @extend_schema(
        summary="Удаление товара из корзины",
        request=ProductCartChangeSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None
        }
    )
    @action(methods=['PUT'], url_path='delete', detail=False)
    def delete_product_cart(self, request):
        """Отдельный эндпоинт для удаления товара из корзины."""
        product = change_product_cart_amount(request)
        context = self.get_serializer_context()
        return list_cart_product(product, context)
