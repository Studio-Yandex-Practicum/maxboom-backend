from rest_framework import serializers

from catalogue.models import Brand, Category, Product, ProductImage


class ImageThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image',)


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
        return super().to_representation(instance)


class ProductSerializer(serializers.ModelSerializer):
    '''Сериализатор для товаров'''
    category = RootSerializer(read_only=True)
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


class FilterProductSerializer(serializers.ListSerializer):
    '''Получение товаров разрешенных для публикации, is_deleted = false'''

    def to_representation(self, data):
        data = data.filter(is_deleted=False)
        return super().to_representation(data)


class ProductWithoutCategoryTreeSerializer(ProductSerializer):
    '''Сериализатор для товаров без дерева категорий'''
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        list_serializer_class = FilterProductSerializer
        model = Product
        fields = ('__all__')


class BrandSerializer(serializers.ModelSerializer):
    '''Сериализатор для производителей.'''
    products = ProductWithoutCategoryTreeSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = (
            'id', 'name', 'slug', 'products', 'image', 'is_prohibited',
            'is_visible_on_main'
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
        return super().to_representation(instance)


class FilterRootCategorySerializer(serializers.ListSerializer):
    '''Получение категории верхнего уровня, root = None'''

    def to_representation(self, data):
        data = data.filter(root=None)
        return super().to_representation(data)


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категорий.'''

    branches = BranchesSerializer(many=True, read_only=True)
    root = RootSerializer(read_only=True)
    products = ProductWithoutCategoryTreeSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterRootCategorySerializer
        model = Category
        fields = (
            'id', 'name', 'slug',
            'meta_title', 'meta_description',
            'products',
            'branches',
            'root',
        )
        read_only_fields = ('products', 'branches', 'root')
