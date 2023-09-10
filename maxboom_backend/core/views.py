from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import (About, Contacts, Requisite, MainShop, OurShop,
                     MailContact, Privacy, Terms,
                     DeliveryInformation, MailContactForm,
                     Header, Footer)
from .serializers import (AboutSerializer,
                          DeliveryInformationSerializer,
                          PrivacySerializer, TermsSerializer,
                          ContactsSerializer, RequisiteSerializer,
                          MainShopSerializer, OurShopSerializer,
                          MailContactSerializer,
                          MailContactFormSerializer,
                          HeaderSerializer, FooterSerializer)


class BaseInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Базовый класс для информационных моделей. Ограничивает
    от создания и редактирования на уровне вью.
    """


class AboutViewSet(BaseInfoViewSet):
    """
    Вьюсет страницы "О нас".
    """

    queryset = About.objects.all()
    serializer_class = AboutSerializer


class DeliveryInformationViewSet(BaseInfoViewSet):
    """
    Вьюсет страницы "Информация о доставке".
    """

    queryset = DeliveryInformation.objects.all()
    serializer_class = DeliveryInformationSerializer


class PrivacyViewSet(BaseInfoViewSet):
    """
    Вьюсет страницы "Политика безопасности".
    """

    queryset = Privacy.objects.all()
    serializer_class = PrivacySerializer


class TermsViewSet(BaseInfoViewSet):
    """
    Вьюсет страницы "Условия соглашения".
    """

    queryset = Terms.objects.all()
    serializer_class = TermsSerializer


# class MailFormViewSet(BaseInfoViewSet):
#     """
#     Вьюсет элементов формы вопроса
#     компании на странице "Контакты".
#     """
#
#     queryset = MailContactForm.objects.all()
#     serializer_class = MailContactFormSerializer
#
#
# class MainShopViewSet(BaseInfoViewSet):
#     """
#     Вьюсет объекта основного магазина
#     на странице "Контакты".
#     """
#
#     queryset = MainShop.objects.all()
#     serializer_class = MainShopSerializer
#
#
# class OurShopsViewSet(BaseInfoViewSet):
#     """
#     Вьюсет объектов дополнительных магазинов
#     на странице "Контакты".
#     """
#
#     queryset = OurShop.objects.all()
#     serializer_class = OurShopSerializer
#
#
# class RequisiteViewSet(BaseInfoViewSet):
#     """
#     Вьюсет объектов реквизитов на странице "Контакты".
#     """
#
#     queryset = Requisite.objects.all()
#     serializer_class = RequisiteSerializer


class ContactsViewSet(BaseInfoViewSet):
    """
    Вьюсет страницы "Контакты".
    """

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

    # Отдельный эндпоинт позволяет по get-запросу получить
    # все запросы на обращение через e-mail и по post-запросу
    # отправить новое.
    @action(methods=['get', 'post'], detail=False,
            url_path='mail')
    def get_mail(self, request):
        if request.method == 'GET':
            queryset = MailContact.objects.all()
            serializer = MailContactSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            data = request.data
            instance = MailContact.objects.create(**data)
            serializer = MailContactSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Временно неопределённый статус у вьюсетов хэдера и футера.
# class HeaderViewSet(BaseInfoViewSet):
#     """
#     Вьюсет для хэдера со всеми его элементами.
#     """
#
#     queryset = Header.objects.all()
#     serializer_class = HeaderSerializer
#
#
# class FooterViewSet(BaseInfoViewSet):
#     """
#     Вьюсет для футера со всеми его элементами.
#     """
#
#     queryset = Footer.objects.all()
#     serializer_class = FooterSerializer


class BaseElementsView(views.APIView):
    """
    Общая вью для хэдера и футера.
    """

    def get(self, request):
        try:
            header = Header.objects.all()[0]
        except IndexError:
            return Response("Отсутствует шапка страницы!")
        header_serializer = HeaderSerializer(
            header, context={'request': request}
        )
        try:
            footer = Footer.objects.all()[0]
        except IndexError:
            return Response("Отсутствует подвал страницы!")
        footer_serializer = FooterSerializer(
            footer, context={'request': request}
        )
        return Response({
            "header": header_serializer.data,
            "footer": footer_serializer.data
            },
            status=status.HTTP_200_OK
        )
