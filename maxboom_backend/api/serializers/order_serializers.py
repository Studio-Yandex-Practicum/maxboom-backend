from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers

from cart.utils import get_cart
from catalogue.models import Product
from order.models import (
    Commodity, CommodityRefund, Order, OrderRefund, OrderReturn
)

User = get_user_model()


class ReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderReturn
        fields = '__all__'

    def validate_order_id(self, value):
        try:
            Order.objects.get(pk=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                f'Заказ: {value}, не найден.'
            )
        return value

    def validate(self, attrs):
        order_id = attrs.get('order_id')
        product_id = attrs.get('product_id')
        quantity = attrs.get('quantity')
        email = attrs.get('email')
        order = Order.objects.get(pk=order_id)
        try:
            commodity = order.commodities.get(
                product__id=product_id
            )
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                f'Код товара: {product_id}, не найден.'
            )
        if commodity.rest < quantity:
            raise serializers.ValidationError(
                f'Количество товара "{commodity.product.name}"'
                ' превышает оставшееся в заказе количество'
            )
        if order.user is None and order.email != email:
            raise serializers.ValidationError(
                f'Заказ: {order_id} с email: {email}  не найден.'
            )
        user = self.context.get('request').user
        if (
            order.user is not None
            and user.is_authenticated
            and user != order.user
        ):
            raise serializers.ValidationError(
                f'Заказ: {order_id} клиента: {user}  не найден.'
            )
        return super().validate(attrs)


class CommodityListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = Commodity
        fields = (
            'id', 'name', 'image', 'quantity', 'price', 'code',
            'product', 'rest'
        )

    def get_name(self, obj):
        return obj.product.name

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.product.images.all().exists():
            image = obj.product.images.all()[0].image.url
            return request.build_absolute_uri(image)
        return None

    def get_price(self, obj):
        return obj.price

    def get_code(self, obj):
        return obj.product.code


class CommodityRefundListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    commodity = serializers.PrimaryKeyRelatedField(
        queryset=CommodityRefund.objects.all()
    )

    class Meta:
        model = Commodity
        fields = (
            'id', 'name', 'image', 'price', 'code',
            'commodity',
            'quantity',
        )

    def get_name(self, obj):
        return obj.commodity.product.name

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.commodity.product.images.all().exists():
            image = obj.commodity.product.images.all()[0].image.url
            return request.build_absolute_uri(image)
        return None

    def get_price(self, obj):
        return obj.commodity.price

    def get_code(self, obj):
        return obj.commodity.product.code


class CommodityRefundSerializer(serializers.ModelSerializer):
    commodity = serializers.PrimaryKeyRelatedField(
        queryset=Commodity.objects.all())

    class Meta:
        model = CommodityRefund
        fields = (
            'commodity', 'refund', 'quantity'
        )
        read_only_fields = ('refund',)

    def __init__(self, order, **kwargs):
        self.order = order
        super().__init__(**kwargs)

    def validate(self, data):
        """
        Проверка максимального доступного для возврата количества
        """
        if data.get('commodity').rest < data.get('quantity'):
            raise serializers.ValidationError(
                {'quantity': ('Количество возвращаемых единиц товара '
                              'больше количества товара, оставшегося '
                              'после осуществленных возвратов '
                              f'({data.get("commodity").rest}).')}
            )
        return data

    def validate_commodity(self, obj):
        """
        Проверка, что товар был в заказе
        """
        if obj not in self.order.commodities.all():
            raise serializers.ValidationError("Товара нет в заказе")
        return obj


class OrderRefundSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    commodities = CommodityRefundListSerializer(
        many=True
    )

    class Meta:
        model = OrderRefund
        fields = (
            'id',
            'order',
            'commodities',
            'value',
            'is_refunded'
        )


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True,)
    commodities = CommodityListSerializer(
        many=True, required=False
    )

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'session_id', 'address',
            'phone', 'email', 'comment', 'value', 'commodities',
            'is_paid', 'status'
        )
        read_only_fields = ('status',)

    @transaction.atomic
    def create(self, validated_data):
        if 'commodities' in self.initial_data:
            validated_data.pop('commodities')
        order = Order.objects.create(**validated_data)
        cart = get_cart(self.context.get('request'))
        for obj in cart.products.all():
            commodity = Commodity(
                product=obj,
                order=order, quantity=obj.productcart_set.get(cart=cart).amount
            )
            try:
                commodity.full_clean()
            except Exception as e:
                raise serializers.ValidationError(f'{e}')
            else:
                commodity.save()
        return order
