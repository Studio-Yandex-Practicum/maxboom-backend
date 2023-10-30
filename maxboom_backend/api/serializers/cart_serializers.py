from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cart.models import Cart, ProductCart


class ProductCartListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = ProductCart
        fields = ('name', 'image', 'price', 'amount', 'full_price')

    def get_name(self, obj) -> str:
        name = obj.product.name
        return name

    def get_image(self, obj) -> str:
        request = self.context.get('request')
        image_url = obj.product.images.all()[0].image.url
        return request.build_absolute_uri(image_url)

    def get_price(self, obj) -> float:
        price = obj.product.price
        return price


class CartSerializer(serializers.ModelSerializer):
    products = ProductCartListSerializer(many=True, source='productcart_set')

    class Meta:
        model = Cart
        fields = ('id', 'products', 'user', 'cart_full_price')


class ProductCartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCart
        fields = ('product', 'cart', 'amount')

    def create(self, validated_data):
        if products := ProductCart.objects.filter(
                cart=validated_data['cart'],
                product=validated_data['product']
        ):
            product = products[0]
            product.amount += validated_data['amount']
            product.save()
            return product
        else:
            return super().create(validated_data)

    def update(self, instance, validated_data):
        if products := ProductCart.objects.filter(
                cart=validated_data['cart'],
                product=validated_data['product']
        ):
            product = products[0]
            product.amount = validated_data['amount']
            product.save()
            return product
        else:
            return super().create(validated_data)
