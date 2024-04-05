from rest_framework import serializers
from drf_spectacular.utils import (
    extend_schema_serializer, extend_schema_field,
)
from rest_framework.exceptions import ValidationError

from api.serializers.catalogue import ProductSerializer
from cart.models import Cart, ProductCart


class ProductCartListSerializer(serializers.ModelSerializer):
    full_price = serializers.FloatField()
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductCart
        fields = ('amount', 'product', 'full_price')


class CartSerializer(serializers.ModelSerializer):
    products = ProductCartListSerializer(many=True, source='productcart_set')
    cart_full_price = serializers.FloatField()

    class Meta:
        model = Cart
        fields = ('id', 'products', 'user', 'cart_full_price')


class ProductCartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCart
        fields = ('product', 'cart', 'amount')

    def create(self, validated_data):
        """Обрабатывает POST и PUT методы вьюсета корзины."""
        action = self.context['request'].method
        if products := ProductCart.objects.filter(
                cart=validated_data['cart'],
                product=validated_data['product']
        ):
            product = products[0]
            if action == 'PUT':
                product.amount = validated_data['amount']
            elif action == 'POST':
                product.amount += validated_data['amount']
            else:
                raise ValidationError("Неподдерживаемый метод.")
            product.save()
            return product
        else:
            return super().create(validated_data)


@extend_schema_serializer(
    exclude_fields=('amount', 'cart')
)
class ProductCartChangeSerializer(ProductCartCreateSerializer):
    """Отдельный сериализатор для отображения запроса
     изменения товара в документации."""
    ...
