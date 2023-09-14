from rest_framework import serializers
from catalogue.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов."""
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "brand",
            "category",
            "code",
            "wb_urls",
            "images",
            "meta_title",
            "meta_description",
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "meta_title", "meta_description", "products")
        read_only_fields = ("products",)
