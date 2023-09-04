from rest_framework import viewsets

from .models import Contacts, Requisite, MainShop, OurShop
from .serializers import ContactsSerializer, RequisiteSerializer, MainShopSerializer, OurShopSerializer


class MainShopViewSet(viewsets.ModelViewSet):
    queryset = MainShop.objects.all()
    serializer_class = MainShopSerializer


class OurShopsViewSet(viewsets.ModelViewSet):
    queryset = OurShop.objects.all()
    serializer_class = OurShopSerializer


class RequisiteViewSet(viewsets.ModelViewSet):
    queryset = Requisite.objects.all()
    serializer_class = RequisiteSerializer


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


