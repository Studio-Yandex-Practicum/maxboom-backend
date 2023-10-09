from django_filters.rest_framework import ModelMultipleChoiceFilter, FilterSet

from rest_framework import filters
from catalogue.models import Category, Product


class CustomProductSearchFilter(filters.SearchFilter):
    """
    Поиск по имени и описанию продукта, если параметр в запросе
    description=True.
    Поиск по имени по умолчанию.
    """

    def get_search_fields(self, view, request):
        description = request.query_params.get('description', False)
        if (
            type(description) is str
            and description.upper() == 'TRUE'
        ):
            return ('name', 'category__name', 'description',)
        return ('name', 'category__name')


class ProductFilterSet(FilterSet):
    """
    Фильтр товаров без учета подкатегорий, если параметр
    в запросе sub_category=False.
    Фильтр продуктов с учетом подкатегорий по умолчанию.
    """
    category = ModelMultipleChoiceFilter(
        field_name='category',
        to_field_name='id',
        queryset=Category.objects.all(),
        method='filter_category_in'
    )

    def filter_category_in(self, queryset, name, value):
        if value:
            sub_category = self.request.query_params.get(
                'sub_category', True)
            if (
                type(sub_category) is str
                and sub_category.upper() == 'FALSE'
            ):
                sub_category = False
            else:
                sub_category = True
            if sub_category:
                category_list = []
                for category in value:
                    self.category_add(
                        category=category, category_list=category_list)
                return queryset.filter(category__in=category_list)
            return queryset.filter(category__in=value)
        return queryset

    def category_add(self, category, category_list):
        if type(category) is Category:
            category_list.append(category)
            if category.branches:
                for item in category.branches.all():
                    self.category_add(
                        category=item, category_list=category_list)

    class Meta:
        model = Product
        fields = (
            'category',
            'brand',
        )
