import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from order.models import Order

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email='test@nn.nn',
            password='12345'
        )
        cls.order = Order.objects.create(
            user=cls.user,
            phone='+79991243684',
            email=cls.user.email,
            address='г.Москва, ул. Ленина, д. 41, к. 2'
        )

    def setUp(self):
        self.user_client = APIClient()
        self.user_authorized_client = APIClient()
        self.user_authorized_client.force_authenticate(
            OrderURLTests.user)

    def test_user_get_urls(self):
        '''доступные пользователям url'''
        order = OrderURLTests.order
        status_pages = {
            '/api/order/': HTTPStatus.OK,
            f'/api/order/{order.id}/': HTTPStatus.OK,
        }
        for address, code in status_pages.items():
            with self.subTest(address=address):
                response = self.user_authorized_client.get(address)
                self.assertEqual(response.status_code, code, f'{address}')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
