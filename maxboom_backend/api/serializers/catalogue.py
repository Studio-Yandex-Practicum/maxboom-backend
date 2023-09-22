from rest_framework import serializers
from catalogue.models import (
    Category, Product, Brand, ProductImage
)


class ImageThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image', 'thumbnail',)


class ProductSimpleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    images = ImageThumbnailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('__all__')


class BrandSerializer(serializers.ModelSerializer):
    '''Сериализатор для производителей.'''
    products = ProductSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = (
            'id', 'name', 'slug', 'products'
        )
        read_only_fields = ('products',)


class BranchesSerializer(serializers.ModelSerializer):
    '''Сериализатор для дочерних категорий'''

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug',
            'branches',
        )

    def to_representation(self, instance):
        self.fields['branches'] = BranchesSerializer(
            read_only=True, many=True,)
        return super(BranchesSerializer, self).to_representation(
            instance)


class RootSerializer(serializers.ModelSerializer):
    '''Сериализатор для родительских категорий'''

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug',
            'root',
        )

    def to_representation(self, instance):
        self.fields['root'] = RootSerializer(
            read_only=True,)
        return super(RootSerializer, self).to_representation(
            instance)


class FilterCategorySerializer(serializers.ListSerializer):
    '''Фильтр категорий'''

    def to_representation(self, data):
        data = [i for i in data if i.root is None]
        return super().to_representation(data)


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий.'''

    branches = BranchesSerializer(many=True, read_only=True)
    root = RootSerializer(read_only=True)
    products = ProductSimpleSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterCategorySerializer
        model = Category
        fields = (
            'id', 'name', 'slug',
            'meta_title', 'meta_description',
            'products',
            'branches',
            'root',
        )
        read_only_fields = ('products', 'branches', 'root')


class ProductSerializer(serializers.ModelSerializer):
    category = RootSerializer(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    images = ImageThumbnailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('__all__')
