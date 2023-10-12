from rest_framework import status, viewsets
from rest_framework.decorators import api_view

from api.filters.catalogue import (
    CustomProductSearchFilter,
    ProductFilterSet
)
from api.serializers.catalogue import (
    BrandSerializer, CategorySerializer,
    CategoryTreeSerializer, ProductSerializer,
)
from catalogue.models import Brand, Category, Product
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter,
    # OpenApiExample
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


@extend_schema(
    tags=["Каталог"],
)
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка категорий',
        description="""Получение списка категорий.
        Применение параметра ordering позволяет
        упорядочить список по  имени (name).
        Применение параметра is_visible_on_main  позволяет
        отфильтровать категории, которые должны отображаться
        на главной странице.
        Применение параметра category_tree  позволяет
        получить отображение категорий с учетом их
        вложенности (false принято по умолчанию).
        Применение параметра search осуществляет поиск по наименованию
        категории.
        Поиск работает по частичным совпадениям без учёта регистра,
        можно искать по нескольким совпадениям:
        в запросе их надо разделить запятыми, без пробелов.
        """,
        parameters=[
            OpenApiParameter(
                name='category_tree',
                location=OpenApiParameter.QUERY,
                description='отображение дерева категорий',
                required=False,
                type=bool
            ),
            OpenApiParameter(
                name='ordering',
                location=OpenApiParameter.QUERY,
                description='способ сортировки',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='search',
                location=OpenApiParameter.QUERY,
                description='поиск по наименованию',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='is_visible_on_main',
                location=OpenApiParameter.QUERY,
                description='запрос категории для главного экрана',
                required=False,
                type=bool
            ),
        ]
    ),
    retrieve=extend_schema(
        summary='Получение отдельной категории',
        parameters=[
            OpenApiParameter(
                name='slug',
                location=OpenApiParameter.PATH,
                description='slug категории',
                required=True,
                type=str
            ),
        ]
    )
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all().prefetch_related(
        'root', 'root__root', 'root__root__root',
        'branches__branches__branches',
        'branches__branches', 'branches',
    ).filter(is_prohibited=False)
    pagination_class = None
    filter_backends = (
        filters.OrderingFilter, DjangoFilterBackend,
        filters.SearchFilter
    )
    filterset_fields = ('is_visible_on_main',)
    ordering_fields = ('name',)
    search_fields = ('name',)

    def get_serializer_class(self):
        category_tree = self.request.query_params.get(
            'category_tree', False)
        if (
            type(category_tree) is str
            and category_tree.upper() == 'TRUE'
        ):
            return CategoryTreeSerializer
        return CategorySerializer


@extend_schema(
    tags=["Каталог"],
)
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка производителей',
        description="""Получение списка производителей,
        Применение параметра ordering позволяет
        упорядочить список по  имени (name).
        Применение параметра is_visible_on_main  позволяет
        отфильтровать производителей, которые должны отображаться
        на главной странице.
        """,
        parameters=[
            OpenApiParameter(
                name='ordering',
                location=OpenApiParameter.QUERY,
                description='способ сортировки',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='is_visible_on_main',
                location=OpenApiParameter.QUERY,
                description='запрос производителей для главного экрана',
                required=False,
                type=bool
            ),
        ]
    ),
    retrieve=extend_schema(
        summary='Получение отдельного производителя',
        parameters=[
            OpenApiParameter(
                name='slug',
                location=OpenApiParameter.PATH,
                description='slug производителя',
                required=True,
                type=str
            ),
        ]
    )
)
class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Brand.objects.all().filter(
        is_prohibited=False)
    serializer_class = BrandSerializer
    pagination_class = None
    filter_backends = (
        filters.OrderingFilter, DjangoFilterBackend,
    )
    filterset_fields = ('is_visible_on_main',)
    ordering_fields = ('name',)

    def get_queryset(self):
        return super().get_queryset()


@extend_schema(
    tags=["Каталог"],
    summary='Каталог',
)
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка товаров',
        description="""Получение списка товаров.
        Применение параметра limit определяет количество товаров на странице.
        Применение параметра offset определяет,
        с какого по счёту товара начать отсчёт.
        Применение параметра ordering позволяет
        упорядочить список по имени, цене, коду товара (name, price, code).
        Применение параметра category  позволяет
        отфильтровать товары определенной (по id) категории.
        Дополнительно параметром sub_category = False можно
        ограничить фильтрацию определенной категорией,
        sub_category = true (true принято по умолчанию) включает в результаты
        запроса товары из подкатегорий.
        Применение параметра brand  позволяет
        отфильтровать товары определенного (по id) производителя.
        Применение параметра search осуществляет поиск по наименованию товара,
        коду товара, наименованию категории товара.
        Поиск работает по частичным совпадениям без учёта регистра,
        можно искать по нескольким совпадениям:
        в запросе их надо разделить запятыми, без пробелов.
        Применение параметра description = True,
        позволяет осуществлять поиск в описаниях товара.
        """,
        parameters=[
            OpenApiParameter(
                name='limit',
                location=OpenApiParameter.QUERY,
                description='количество товаров на странице',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='offset',
                location=OpenApiParameter.QUERY,
                description='определяет с какого товара начать отсчёт',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='brand',
                location=OpenApiParameter.QUERY,
                description=(
                    'id производителя, товары которого необходимо получить'
                ),
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='ordering',
                location=OpenApiParameter.QUERY,
                description='способ сортировки',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='search',
                location=OpenApiParameter.QUERY,
                description='поиск по наименованию товара',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='description',
                location=OpenApiParameter.QUERY,
                description='поиск в описаниях товаров',
                required=False,
                type=bool
            ),
            OpenApiParameter(
                name='category',
                location=OpenApiParameter.QUERY,
                description='id категории, товары которой необходимо получить',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='sub_category',
                location=OpenApiParameter.QUERY,
                description='отображать товары подкатегорий',
                required=False,
                type=bool
            ),
        ]
    ),
    retrieve=extend_schema(
        summary='Получение отдельного товара',
        parameters=[
            OpenApiParameter(
                name='slug',
                location=OpenApiParameter.PATH,
                description='slug товара',
                required=True,
                type=str
            ),
        ]
    )
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Product.objects.all().prefetch_related(
        'category', 'category__branches',
        'category__branches__branches', 'images',
    ).filter(is_deleted=False, category__is_prohibited=False)
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        CustomProductSearchFilter,
    )
    filterset_class = ProductFilterSet
    ordering_fields = ('name', 'code', 'price')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='sub_category',
                location=OpenApiParameter.QUERY,
                description='включая подкатегории',
                required=False,
                type=bool
            ),
            OpenApiParameter(
                name='description',
                location=OpenApiParameter.QUERY,
                description='включая поиск в описании товаров',
                required=False,
                type=bool
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=["Каталог"],
    summary='Поиск в категориях и товарах',
    description="""Получение списка категорий и товаров,
    удовлетворяющих условиям поиска, параметр search.
    Поиск работает по частичным совпадениям без учёта регистра,
    можно искать по нескольким совпадениям:
    в запросе их надо разделить запятыми, без пробелов.
    Применение параметра ordering позволяет
    упорядочить список категорий по  имени (name),
    список товаров по имени, цене, коду товара (name, price, code).
    Применение параметра category позволяет
    провести поиск товара в определенной (по id) категории.
    Дополнительно параметром sub_category = False можно
    ограничить поиск товара определенной категорией (без подкатегорий),
    sub_category = true (true принято по умолчанию) включает в результаты
    запроса товары из подкатегорий.
    Применение параметра description = True,
    позволяет осуществлять поиск в описаниях товара.
    Применение параметра limit определяет количество товаров на странице.
    Применение параметра offset определяет,
    с какого по счёту товара начать отсчёт.
    """,
    parameters=[
        OpenApiParameter(
            name='search',
            location=OpenApiParameter.QUERY,
            description='поиск по наименованию',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='description',
            location=OpenApiParameter.QUERY,
            description='поиск в описаниях товаров',
            required=False,
            type=bool
        ),
        OpenApiParameter(
            name='category',
            location=OpenApiParameter.QUERY,
            description='id категории, в которой провести поиск товаров',
            required=False,
            type=int
        ),
        OpenApiParameter(
            name='sub_category',
            location=OpenApiParameter.QUERY,
            description='провести поиск в подкатегориях',
            required=False,
            type=bool
        ),
        OpenApiParameter(
            name='ordering',
            location=OpenApiParameter.QUERY,
            description='способ сортировки',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='limit',
            location=OpenApiParameter.QUERY,
            description='количество товаров на странице',
            required=False,
            type=int
        ),
        OpenApiParameter(
            name='offset',
            location=OpenApiParameter.QUERY,
            description='определяет с какого товара начать отсчёт',
            required=False,
            type=int
        ),
    ]
)
@api_view(('GET',))
def search(request, *args, **kwargs):
    resp_category = CategoryViewSet.as_view(
        actions={'get': 'list'},
    )(request=request._request, *args, **kwargs)
    resp_product = ProductViewSet.as_view(
        actions={'get': 'list'},
    )(request=request._request, *args, **kwargs)
    data = {}
    if (
        resp_category.status_code == status.HTTP_400_BAD_REQUEST
        and resp_product.status_code == status.HTTP_400_BAD_REQUEST
    ):
        return Response(
            'Поиск не возможен', status=status.HTTP_400_BAD_REQUEST)
    if (resp_category.status_code == status.HTTP_200_OK):
        data['category'] = resp_category.render().data
    else:
        data['category'] = []
    if (resp_product.status_code == status.HTTP_200_OK):
        data['product'] = resp_product.render().data
    else:
        data['product'] = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }
    return Response(data=data, status=status.HTTP_200_OK,)
