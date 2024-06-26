from rest_framework import serializers

from catalogue.models import Brand, Category, Product, ProductImage
from maxboom.settings import DISCOUNT_ANONYM, DISCOUNT_USER


class ImageThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров"""
    category = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    images = ImageThumbnailSerializer(read_only=True, many=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = ('__all__')
        exclude = ('vendor_code', 'imt_id')

    def get_price(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and user.userprofile.is_vendor:
            return round(obj.price * DISCOUNT_USER, 2)
        return round(obj.price * DISCOUNT_ANONYM, 2)


class BrandSerializer(serializers.ModelSerializer):
    """Сериализатор для производителей."""

    class Meta:
        model = Brand
        fields = (
            'id', 'name', 'slug', 'image', 'is_prohibited',
            'is_visible_on_main'
        )


class FilterBranchesCategorySerializer(serializers.ListSerializer):
    """
    Получение подкатегорий разрешенных для публикации, is_prohibited = False
    """

    def to_representation(self, data):
        data = data.filter(is_prohibited=False)
        return super().to_representation(data)


class BranchSerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий"""
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug',
            'products_count',
            'branches',
        )
        list_serializer_class = FilterBranchesCategorySerializer

    def to_representation(self, instance):
        self.fields['branches'] = BranchSerializer(
            read_only=True, many=True,)
        return super().to_representation(instance)

    def get_products_count(self, obj):
        return obj.products.count()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    branches = serializers.StringRelatedField(many=True, read_only=True)
    root = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug',
            'branches',
            'root', 'is_prohibited',
            'is_visible_on_main',
            'image'
        )
        read_only_fields = ('branches', 'root')


class FilterRootCategorySerializer(serializers.ListSerializer):
    """Получение категории верхнего уровня, root = None"""

    def to_representation(self, data):
        data = data.filter(root=None)
        return super().to_representation(data)


class RootSerializer(serializers.ModelSerializer):
    """Сериализатор для родительских категорий"""

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug',
            'root',
        )

    def to_representation(self, instance):
        self.fields['root'] = RootSerializer(
            read_only=True,)
        return super().to_representation(instance)


class CategoryTreeSerializer(CategorySerializer):
    """Сериализатор для категорий с учетом вложенности."""

    branches = BranchSerializer(many=True, read_only=True)
    root = RootSerializer(read_only=True)
    total_count = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilterRootCategorySerializer
        model = Category
        fields = (
            'id', 'name', 'slug',
            'total_count',
            'branches',
            'root', 'is_prohibited',
            'is_visible_on_main',
            'image'
        )
        read_only_fields = ('branches', 'root')

    def get_total_count(self, obj):
        total_count = obj.products.count()
        query_categories = Category.objects.all().prefetch_related(
            'root', 'root__root', 'root__root__root',
            'branches__branches__branches',
            'branches__branches', 'branches',).filter(is_prohibited=False
                                                      ).filter(root=obj)
        for category in query_categories:
            total_count += category.products.count()
        return total_count
