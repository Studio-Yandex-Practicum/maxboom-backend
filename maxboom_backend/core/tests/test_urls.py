# flake8: noqa
from http import HTTPStatus

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


class InfoPageTestCase(TestCase):

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

    def test_anonymous_url_access(self):
        """Проверка доступа для анонимных пользователей."""
        pages_statuses = {
            '/api/core/about/': HTTPStatus.OK,
            '/api/core/information/': HTTPStatus.OK,
            '/api/core/privacy/': HTTPStatus.OK,
            '/api/core/terms/': HTTPStatus.OK,
            '/api/core/contacts/': HTTPStatus.OK,
            '/api/core/contacts/mail/': HTTPStatus.UNAUTHORIZED,
            '/api/core/base/': HTTPStatus.OK
        }
        for url, status in pages_statuses.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_anonymous_user_mail_contact_post(self):
        """Проверка отправки анонимным пользователем обращения по форме."""
        mail_url = '/api/core/contacts/mail/'
        post_data = {
            'person_name': 'Тест Тестович',
            'person_email': 'test@test.test',
            'message': 'Тестовое обращение 2'
        }
        response = self.client.post(
            mail_url,
            data=post_data
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_superuser_mail_access(self):
        """Проверка доступа обращений для суперпользователей."""
        page = '/api/core/contacts/mail/'
        response = self.admin_client.get(page)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def tearDown(self):
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

