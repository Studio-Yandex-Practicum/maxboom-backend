from rest_framework import serializers

from core.models import (About, Privacy, DeliveryInformation,
                         Contacts, Requisite, MainShop, OurShop,
                         MailContact, MailContactForm,
                         Header, Footer, Support, Terms)


class BaseCoreSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор для core-моделей.
    Наследующиеся от него также наследуют метакласс,
    чтобы исключить поле 'id'.
    """

    class Meta:
        exclude = ['id']


class BaseInfoModelSerializer(BaseCoreSerializer):
    """
    Базовый сериализатор для моделей информационных страниц.
    """

    headline = serializers.CharField(read_only=True)
    text = serializers.CharField(read_only=True)
    meta_title = serializers.CharField(read_only=True)
    meta_description = serializers.CharField(read_only=True)


class AboutSerializer(BaseInfoModelSerializer):
    """
    Сериализатор страницы "О нас".
    """

    class Meta(BaseCoreSerializer.Meta):
        model = About


class DeliveryInformationSerializer(BaseInfoModelSerializer):
    """
    Сериализатор страницы "Информация о доставке".
    """

    class Meta(BaseCoreSerializer.Meta):
        model = DeliveryInformation


class PrivacySerializer(BaseInfoModelSerializer):
    """
    Сериализатор страницы "Политика безопасности".
    """

    class Meta(BaseCoreSerializer.Meta):
        model = Privacy


class TermsSerializer(BaseInfoModelSerializer):
    """
    Сериализатор страницы "Условия соглашения".
    """

    class Meta(BaseCoreSerializer.Meta):
        model = Terms


class MailContactFormSerializer(BaseCoreSerializer):
    """
    Сеариализатор формы запроса для страницы "Контакты".
    """

    class Meta(BaseCoreSerializer.Meta):
        model = MailContactForm
        exclude = ['id', 'main_page']


class RequisiteSerializer(BaseCoreSerializer):
    """
    Сериализатор модели реквизитов для страницы "Контакты".
    """

    class Meta(BaseCoreSerializer.Meta):
        model = Requisite
        exclude = ['id', 'main_page']


class BaseShopSerializer(serializers.ModelSerializer):
    """
    Сариализатор базовой модели элемента магазина на странице
    "Контакты", от которого наследуются следующие.
    """

    name = serializers.CharField(read_only=True)
    comment = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True)

    class Meta:
        exclude = ['id', 'main_page']


class MainShopSerializer(BaseShopSerializer):
    """
    Сериализатор основного магазина.
    """

    email = serializers.CharField(read_only=True)
    location = serializers.CharField(read_only=True)

    class Meta(BaseShopSerializer.Meta):
        model = MainShop


class OurShopSerializer(BaseShopSerializer):
    """
    Сериализатор дополнительных магазинов.
    """

    photo = serializers.ImageField(read_only=True)
    is_main_shop = serializers.BooleanField(read_only=True)

    class Meta(BaseShopSerializer.Meta):
        model = OurShop


class ContactsSerializer(BaseCoreSerializer):
    """
    Сериализатор страницы контактов.
    """

    main_shop = serializers.SerializerMethodField(read_only=True)
    requisites = serializers.SerializerMethodField(read_only=True)
    mail_form = serializers.SerializerMethodField(read_only=True)
    our_shops = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseCoreSerializer.Meta):
        model = Contacts

    def get_requisites(self, value):
        requisites = value.requisites.all()
        return RequisiteSerializer(requisites, many=True).data

    def get_main_shop(self, value):
        try:
            main_shop = value.main_shop.all()[0]
        except IndexError:
            return "Отсутствует основной магазин!"
        return MainShopSerializer(main_shop).data

    def get_mail_form(self, value):
        try:
            mail_form = value.mail_form.all()[0]
        except IndexError:
            return "Отсутствуют поля формы обращения!"
        return MailContactFormSerializer(mail_form).data

    def get_our_shops(self, value):
        our_shops = value.our_shops.all()
        return OurShopSerializer(our_shops, many=True).data


class MailContactSerializer(serializers.Serializer):
    """
    Сериализатор объектов вопросов к магазину.
    """

    id = serializers.SerializerMethodField(read_only=True)
    person_name = serializers.CharField(read_only=True)
    person_email = serializers.EmailField(read_only=True)
    message = serializers.CharField(read_only=True)

    class Meta:
        model = MailContact

    def get_id(self, value):
        return f"ID обращения: {value.pk}"


class LogoSerializer(serializers.Serializer):
    """
    Сериализатор для всех логотипов.
    """

    image = serializers.ImageField(read_only=True)
    url = serializers.URLField(read_only=True)

    class Meta:
        fields = ['image', 'url']


class SupportSerializer(BaseCoreSerializer):
    """
    Сериализатор блока "Поддержка" хэдера и футера.
    """

    name = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True)

    class Meta:
        model = Support
        fields = ['name', 'phone_number']


class HeaderSerializer(BaseCoreSerializer):
    """
    Сериализатор хэдера. Цепляет методами все
    связанные с ним данные.
    """

    main_logo = serializers.SerializerMethodField(read_only=True)
    support = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseCoreSerializer.Meta):
        model = Header

    def get_main_logo(self, value):
        try:
            main_logo = value.main_logo.all()[0]
        except IndexError:
            return "Отсутствует основной логотип!"
        return LogoSerializer(main_logo, context=self.context).data

    def get_support(self, value):
        try:
            support = value.support.all()[0]
        except IndexError:
            return "Отсутствует информация о поддержке!"
        return SupportSerializer(support).data


class FooterSerializer(BaseCoreSerializer):
    """
    Сериализатор футера. Помимо своих данных цепляет
    методами связанные с ним данные.
    """

    company_info = serializers.CharField(read_only=True)
    disclaimer = serializers.CharField(read_only=True)
    support_work_time = serializers.CharField(read_only=True)
    main_logo = serializers.SerializerMethodField(read_only=True)
    additional_logos = serializers.SerializerMethodField(read_only=True)
    support = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseCoreSerializer.Meta):
        model = Footer

    def get_main_logo(self, value):
        try:
            main_logo = value.main_logo.all()[0]
        except IndexError:
            return "Отсутствует основной логотип!"
        context = self.context
        return LogoSerializer(main_logo, context=context).data

    def get_additional_logos(self, value):
        additional_logos = value.additional_logos.all()
        context = self.context
        return LogoSerializer(additional_logos, context=context, many=True).data

    def get_support(self, value):
        try:
            support = value.support.all()[0]
        except IndexError:
            return "Отсутствует информация о поддержке!"
        return SupportSerializer(support).data
