from django.urls import include, path
from rest_framework import routers

from api.views.core import (AboutViewSet, ContactsViewSet,
                            DeliveryInformationViewSet, TermsViewSet,
                            PrivacyViewSet, BaseElementsView,
                            # MailFormViewSet, MainShopViewSet,
                            # OurShopsViewSet,
                            # RequisiteViewSet,
                            # HeaderViewSet, FooterViewSet
                            )


router = routers.DefaultRouter()
router.register(r'about', AboutViewSet)
router.register(r'information', DeliveryInformationViewSet)
router.register(r'privacy', PrivacyViewSet)
router.register(r'terms', TermsViewSet)
router.register(r'contacts', ContactsViewSet)
# router.register(r'mailform', MailFormViewSet)
# router.register(r'mainshop', MainShopViewSet)
# router.register(r'ourshops', OurShopsViewSet)
# router.register(r'requisites', RequisiteViewSet)
# router.register(r'header', HeaderViewSet)
# router.register(r'footer', FooterViewSet)

urlpatterns = [
    path('core/base/', BaseElementsView.as_view()),
    path('core/', include(router.urls))
]
