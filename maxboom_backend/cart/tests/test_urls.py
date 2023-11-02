# flake8: noqa
from http import HTTPStatus

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


class CartTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser = User.objects.create_superuser(
            'test@test.test', 'test'
        )

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.force_login(user=self.superuser)

    # def test_get_url_access(self):
    #     """Проверка доступа."""
    #     pages_statuses = {
    #         '/api/cart/': HTTPStatus.OK,
    #     }
    #     for url, status in pages_statuses.items():
    #         with self.subTest(url=url):
    #             response = self.client.get(url)
    #             self.assertEqual(response.status_code, status)

    def tearDown(self):
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
