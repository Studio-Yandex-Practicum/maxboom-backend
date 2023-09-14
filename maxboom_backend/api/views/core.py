from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response


from core.models import (
    About, Contacts, MailContact, Privacy, Terms,
    DeliveryInformation, Header, Footer
)
from api.serializers.core import (
    AboutSerializer, DeliveryInformationSerializer,
    PrivacySerializer, TermsSerializer, ContactsSerializer,
    MailContactSerializer, HeaderSerializer, FooterSerializer
)
from api.permissions.core import IsAdminOrPostOnly


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
            url_path='mail', permission_classes=[IsAdminOrPostOnly])
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
