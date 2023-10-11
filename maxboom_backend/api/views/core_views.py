from rest_framework import viewsets, status, views, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import (extend_schema, OpenApiExample,
                                   OpenApiResponse, PolymorphicProxySerializer)

from core.models import (
    About, Contacts, MailContact, Privacy, Terms,
    DeliveryInformation, Header, Footer
)
from api.serializers.core_serializers import (
    AboutSerializer, DeliveryInformationSerializer,
    PrivacySerializer, TermsSerializer, ContactsSerializer,
    MailContactSerializer, HeaderSerializer, FooterSerializer,
    BaseSerializer
)
from api.permissions.core_permissions import IsAdminOrPostOnly


class BaseInfoViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    Базовый класс для информационных моделей. Ограничивает
    от создания и редактирования на уровне вью.
    """


class AboutViewSet(BaseInfoViewSet):
    """
    Страница "О нас".
    """

    queryset = About.objects.all()
    serializer_class = AboutSerializer


class DeliveryInformationViewSet(BaseInfoViewSet):
    """
    Страница "Информация о доставке".
    """

    queryset = DeliveryInformation.objects.all()
    serializer_class = DeliveryInformationSerializer


class PrivacyViewSet(BaseInfoViewSet):
    """
    Страница "Политика безопасности".
    """

    queryset = Privacy.objects.all()
    serializer_class = PrivacySerializer


class TermsViewSet(BaseInfoViewSet):
    """
    Страница "Условия соглашения".
    """

    queryset = Terms.objects.all()
    serializer_class = TermsSerializer


class ContactsViewSet(BaseInfoViewSet):
    """
    Страница "Контакты".
    """

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

    # Отдельный эндпоинт позволяет по get-запросу получить
    # все запросы на обращение через e-mail и по post-запросу
    # отправить новое.
    @extend_schema(
        description='Получить текущие запросы обратной связи',
        responses={status.HTTP_200_OK: MailContactSerializer(many=True)},
        methods=['get']
    )
    @extend_schema(
        methods=['post'],
        request=MailContactSerializer,
        description='Отправить запрос обратной связи',
        responses={
            status.HTTP_201_CREATED: MailContactSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description='Bad request')
        },
    )
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
    Общее представление для хэдера и футера.
    """

    @extend_schema(
        responses={
            status.HTTP_200_OK: BaseSerializer
        }
    )
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
