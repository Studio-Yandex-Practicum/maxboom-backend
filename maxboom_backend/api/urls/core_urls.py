from django.urls import include, path
from rest_framework import routers

from api.views.core_views import (
    AboutViewSet, ContactsViewSet, DeliveryInformationViewSet,
    TermsViewSet, PrivacyViewSet, BaseElementsView
)


router = routers.DefaultRouter()
router.register(r'about', AboutViewSet)
router.register(r'information', DeliveryInformationViewSet)
router.register(r'privacy', PrivacyViewSet)
router.register(r'terms', TermsViewSet)
router.register(r'contacts', ContactsViewSet)

urlpatterns = [
    path('core/base/', BaseElementsView.as_view()),
    path('core/', include(router.urls))
]
