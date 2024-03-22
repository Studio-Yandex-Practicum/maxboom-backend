from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from catalogue.models import Category


class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_category_name(self):
        category = int(self.request.query_params.get('category', False))
        if category:
            return Category.objects.get(pk=category).name
        return category

    def get_paginated_response(self, data):
        category_name = self.get_category_name()
        if category_name:
            return Response(OrderedDict([
                ('category_name', category_name),
                ('count', self.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data)
            ]))
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
