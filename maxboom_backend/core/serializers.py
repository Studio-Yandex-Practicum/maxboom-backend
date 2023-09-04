from rest_framework import serializers

from .models import BaseCoreModel, About, Policy, Agreements, DeliveryInformation, Contacts, Requisite, \
    MainShop, OurShop, BaseShop


class BaseCoreModelSerializer(serializers.ModelSerializer):
    headline = serializers.CharField(read_only=True)
    text = serializers.CharField(read_only=True)

    class Meta:
        model = BaseCoreModel


class AboutSerializer(BaseCoreModelSerializer):

    class Meta:
        model = About
        fields = ['headline', 'text']


class PolicySerializer(BaseCoreModelSerializer):

    class Meta:
        model = Policy
        fields = ['headline', 'text']


class AgreementsSerializer(BaseCoreModelSerializer):

    class Meta:
        model = Agreements
        fields = ['headline', 'text']


class DeliveryInformationSerializer(BaseCoreModelSerializer):

    class Meta:
        model = DeliveryInformation
        fields = ['headline', 'text']


class RequisiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requisite
        fields = ['requisite_name', 'requisite_description']


class BaseShopSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    comment = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = BaseShop


class MainShopSerializer(BaseShopSerializer):
    email = serializers.CharField()
    location = serializers.CharField()

    class Meta:
        model = MainShop
        fields = ['name', 'comment', 'phone_number', 'email', 'location']


class OurShopSerializer(BaseShopSerializer):
    photo = serializers.ImageField()
    is_main_shop = serializers.BooleanField()

    class Meta:
        model = OurShop
        fields = ['name', 'comment', 'phone_number', 'photo', 'is_main_shop']


class ContactsSerializer(BaseCoreModelSerializer):
    text = None
    requisites = serializers.SerializerMethodField(read_only=True)
    main_shop = serializers.SerializerMethodField(read_only=True)
    our_shops = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contacts
        read_only_fields = ['headline', 'requisites', 'main_shop', 'our_shops']
        exclude = ['id', 'text']

    def get_requisites(self, value):
        requisites = value.requisites.all()
        return RequisiteSerializer(requisites, many=True).data

    def get_main_shop(self, value):
        main_shop = value.main_shop.all()[0]
        return MainShopSerializer(main_shop).data

    def get_our_shops(self, value):
        our_shops = value.our_shops.all()
        return OurShopSerializer(our_shops, many=True).data

