import uuid
from typing import Optional

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.cart_serializers import (
    ProductCartListSerializer, ProductCartCreateSerializer
)
from cart.models import Cart, ProductCart


User = get_user_model()


def get_session(request: Request) -> str:
    """Получить или присвоить сессии UUID."""
    if session := request.session.get('anonymous_id'):
        return session
    else:
        request.session['anonymous_id'] = str(uuid.uuid4())
        return request.session['anonymous_id']


def create_cart(request: Request, active=False) -> Cart:
    """Создаёт новый объект корзины согласно заданным условиям."""
    session = get_session(request)
    user = None
    if active:
        user = request.user
        session = None
    cart = Cart.objects.create(
        user=user,
        session_id=session,
        is_active=active
    )
    return cart


def update_user_cart(cart: Cart, request: Request) -> Cart:
    """Обновляет статус корзины при авторизации."""
    if not cart.user:
        cart.user = request.user
    cart.is_active = True
    cart.session_id = None
    cart.save()
    return cart


def get_cart(request: Request) -> Cart:
    """
    Получает нужную корзину, создает новую или
    переносит из неавторизованной сессии в авторизованную.
    """
    if isinstance(request.user, User):
        # Механизм либо сразу находит корзину пользователя, либо ищет по
        # сессии, либо создаёт новую. Во всех случаях корзины становятся
        # активными и session_id у них становится None, чтобы к ним
        # не было доступа по сессии у неавторизованных пользователей.
        if carts := Cart.objects.filter(
                user=request.user
        ):
            cart = carts[0]
            return cart
        elif carts := Cart.objects.filter(
                session_id=get_session(request)
        ):
            cart = carts[0]
            return update_user_cart(cart, request)
        else:
            return create_cart(request, active=True)
    # Неавторизованная корзина ищется по сессии, так как подразумевается,
    # что любая авторизованная корзина сессии не имеет.
    if carts := Cart.objects.filter(
            session_id=get_session(request)
    ):
        cart = carts[0]
        return cart
    else:
        return create_cart(request)


def process_cart_product(
        request: Request,
        context: dict,
) -> Response:
    """Создаёт или обновляет модель продукта в корзине."""
    action = request.method
    action_responses = {
        'POST': status.HTTP_201_CREATED,
        'PUT': status.HTTP_206_PARTIAL_CONTENT
    }
    cart = get_cart(request)
    product = int(request.data.get('product'))
    amount = int(request.data.get('amount'))
    serializer = ProductCartCreateSerializer(
        data={
            'cart': cart.pk,
            'product': product,
            'amount': amount
        },
        context=context
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        serializer.data,
        status=action_responses[action]
    )


def change_product_cart_amount(request) -> Optional[ProductCart]:
    """Изменяет количество товара в корзине на единицу.
    Удаляет товар из корзины, если его количество станет нулевым."""
    cart = get_cart(request)
    product_id = int(request.data.get('product'))
    if products := ProductCart.objects.filter(
            product=product_id,
            cart=cart,
    ):
        product = products[0]
        action = request.path.split('/')[3]
        if action == 'add':
            product.amount += 1
        elif action == 'subtract':
            if product.amount == 1:
                product.delete()
                return None
            product.amount -= 1
        else:
            product.delete()
            return None
        product.save()
        return product
    else:
        raise ValidationError("Товар отсутствует в корзине!")


def list_cart_product(product: ProductCart, context: dict) -> Response:
    """Обрабатывает объект продукта в корзине"""
    serializer = ProductCartListSerializer(
        product,
        context=context
    )
    return Response(
        serializer.data, status=status.HTTP_206_PARTIAL_CONTENT
    )
