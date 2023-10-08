from rest_framework import serializers

from catalogue.models import Brand, Category, Product, ProductImage


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
        fields = ('__all__')

    def get_price(self, obj):
        if self.context['request'].user.is_authenticated:
            return round(float(obj.price) * 0.5, 2)
        return round(float(obj.price) * 0.8, 2)


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

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug',
            'branches',
        )
        list_serializer_class = FilterBranchesCategorySerializer

    def to_representation(self, instance):
        self.fields['branches'] = BranchSerializer(
            read_only=True, many=True,)
        return super().to_representation(instance)


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
            'is_visible_on_main'
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

    class Meta:
        list_serializer_class = FilterRootCategorySerializer
        model = Category
        fields = (
            'id', 'name', 'slug',
            'branches',
            'root', 'is_prohibited',
            'is_visible_on_main'
        )
        read_only_fields = ('branches', 'root')
