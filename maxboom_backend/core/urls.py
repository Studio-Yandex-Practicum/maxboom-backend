from django.urls import include, path
from rest_framework import routers

from .views import ContactsViewSet, MainShopViewSet, OurShopsViewSet, RequisiteViewSet

router = routers.DefaultRouter()
router.register(r'contacts', ContactsViewSet)
router.register(r'requisites', RequisiteViewSet)
router.register(r'mainshop', MainShopViewSet)
router.register(r'ourshops', OurShopsViewSet)

urlpatterns = [
    path('core/', include(router.urls))
]
