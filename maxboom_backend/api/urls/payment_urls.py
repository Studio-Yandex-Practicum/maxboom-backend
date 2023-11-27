from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.payment_views import OrderPaymentView, RepaymentView

app_name = 'payment'
router = DefaultRouter()
router.register(
    r'order/(?P<order>\d+)/payment',
    OrderPaymentView,
    basename='payment'
)
router.register(
    (r'order/(?P<order>\d+)/refund/(?P<refund>\d+)/'
     'repayment'),
    RepaymentView,
    basename='repayment'
)

urlpatterns = [
    path('', include(router.urls)),
]
