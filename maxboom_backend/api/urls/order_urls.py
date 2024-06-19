from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.order_views import (OrderCancelViewSet, OrderRefundViewSet,
                                   OrderViewSet, ReturnViewSet)

app_name = 'order'
router = DefaultRouter()
router.register(r'order/add-return',
                ReturnViewSet, basename='add_return')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'order/(?P<order>\d+)/refund',
                OrderRefundViewSet, basename='oder_refund')
router.register(r'order/(?P<order>\d+)/cancel',
                OrderCancelViewSet, basename='oder_cancel')
urlpatterns = [
    path('', include(router.urls)),
]
