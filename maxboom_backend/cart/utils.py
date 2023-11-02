import uuid

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from cart.models import Cart, ProductCart


User = get_user_model()


def get_session(request: Request) -> str:
    """Получить или присвоить сессии UUID."""
    if session := request.session.get('anonymous_id'):
        return session
    else:
        request.session['anonymous_id'] = str(uuid.uuid4())
        return session


def get_cart(request: Request) -> Cart:
    """
    Получить нужную корзину, создать новую или
    перенести из неавторизованной сессии в авторизованную.
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
            cart.is_active = True
            cart.session_id = None
            cart.save()
            return cart
        elif carts := Cart.objects.filter(
                session_id=str(get_session(request))
        ):
            cart = carts[0]
            cart.user = request.user
            cart.is_active = True
            cart.session_id = None
            cart.save()
            return cart
        else:
            cart = Cart.objects.create(
                user=request.user,
                is_active=True,
                session_id=None
            )
            return cart
    # Корзины со статусом is_active недоступны для неавторизованных
    # пользователей, поэтому для них сразу создаётся отдельная новая.
    if carts := Cart.objects.filter(
            session_id=get_session(request)
    ):
        cart = carts[0]
        if not cart.is_active:
            return cart
        else:
            cart = Cart.objects.create(
                session_id=get_session(request)
            )
            return cart
    else:
        cart = Cart.objects.create(
            session_id=get_session(request)
        )
        return cart


def change_product_cart_amount(request) -> ProductCart:
    cart = get_cart(request)
    product_id = int(request.data.get('product'))
    if products := ProductCart.objects.filter(
            product=product_id,
            cart=cart,
    ):
        product = products[0]
        if request.path.split('/')[3] == 'add':
            product.amount += 1
        else:
            if product.amount >= 1:
                product.amount -= 1
            else:
                pass
        product.save()
        return product
    else:
        raise ValidationError("Отсутствует товар в корзине!")
