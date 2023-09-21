from rest_framework import serializers
# from .catalogue import CategorySerializer
from catalogue.models import (
    Category, Product, Brand, CategoryTree, ProductImage
)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image',)


class ImageThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image', 'thumbnail',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    images = ImageThumbnailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('__all__')


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    '''Сериализатор для производителей.'''
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = (
            'id', 'name', 'slug', 'products'
        )
        read_only_fields = ('products',)
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


# class CatRootSerializer(serializers.ModelSerializer):
#     roots = 'RootSerializer'(many=True, read_only=True)

#     class Meta:
#         model = Category
#         fields = ('name', 'roots')


# class RootSerializer(serializers.ModelSerializer):
#     '''Сериализатор для родительских категорий'''
#     # root = CategorySerializer(read_only=True, many=True)
#     root = CatRootSerializer(many=True, read_only=True)
#     # root = serializers.SlugRelatedField(
#     #     read_only=True,
#     #     slug_field='name'
#     # )

#     class Meta:
#         model = CategoryTree
#         fields = ('root',)


# class CatAffilSerializer(serializers.ModelSerializer):
#     # branches = 'AffiliatedSerializer'(many=True, read_only=True)

#     class Meta:
#         model = Category
#         fields = ('name', 'branches')


class BranchesSerializer(serializers.Serializer):
    '''Сериализатор для дочерних категорий'''

    # branch = CatAffilSerializer(many=True, read_only=True)

    # class Meta:
    #     model = CategoryTree
    #     fields = ('branch',)
    def to_representation(self, instance):
        serializers = instance.branch.__class__(
            instance, context=self.context)
        return serializers.data
        return super().to_representation(instance)


class CategoryProductSerializer((serializers.HyperlinkedModelSerializer)):
    '''Сериализатор для категорий.'''
    # products = ProductSerializer(many=True, read_only=True)

    branches = BranchesSerializer(many=True, read_only=True)
    # root = RootSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'meta_title', 'meta_description',
            # 'products',
            'branches',
            # 'root',
        )
        # read_only_fields = ('products', 'branches', 'root')
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий.'''
    # branches = AffiliatedSerializer(many=True, read_only=True)
    # root = RootSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'name',
            # 'branches', 'root',
        )
        # read_only_fields = ('branches', 'root')


class ImageHyperlinkSerializer(serializers.HyperlinkedRelatedField):
    view_name = 'product-image'
    # lookup_field = 'image'

    # def to_representation(self, obj):
    #     return obj.image.path


class ImageSerializer(serializers.ModelSerializer):
    images = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='image'
    )


class ImageCustomSerializer(serializers.RelatedField):
    def to_representation(self, obj):
        return obj.image.url


class ProductNewSerializer(serializers.ModelSerializer):
    '''Сериализатор для продуктов.'''
    # images = ImageHyperlinkSerializer(many=True, read_only=True)
    # dict image: url некорректный
    # images = ImageCustomSerializer(many=True, read_only=True)

    # dict image: url
    images = ProductImageSerializer(many=True, read_only=True)

    # ошибка utf-8 символа codec can't decode byte 0x89 in position 0
    # images = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='image'
    # )

    # list pk
    # images = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='pk'
    # )

    # images = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='product-image',
    #     # queryset=Product.objects.all()
    #     lookup_filed='image'
    # )
    # images = ImageHyperlinkSerializer(many=True, read_only=True)

    # roots = RootSerializer(read_only=True,)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'price',
            'brand',
            'category',
            'code',
            'wb_urls',
            'images',

            'meta_title',
            'meta_description',
            # 'roots'
        )
        read_only_fields = (
            'id',
            'slug',
            'images',

            # 'roots',
            'category'
        )
