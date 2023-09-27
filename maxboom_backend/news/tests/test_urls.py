from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from news.models import News


class NewsUrlTests(TestCase):
    """
    Тестирование эндпоинтов приложения news.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.news = News.objects.create(
            title='Заголовок для тестов',
            text='Текст для тестов',
            slug='test-slug',
            meta_title='Мета-заголовок новости',
            meta_description='Мета-описание новости')

    def setUp(self):
        self.user_client = APIClient()

    def test_blog_urls_for_unauthenticated(self):
        """
        Тестирование доступа к эндпоинтам приложения news
        для неавторизованных пользователей.
        """

        news = NewsUrlTests.news
        pages_statuses = {
            '/api/shopnews/': status.HTTP_200_OK,
            f'/api/shopnews/{news.slug}/': status.HTTP_200_OK,
        }
        for url, code in pages_statuses.items():
            with self.subTest(url=url):
                response = self.user_client.get(url)
                self.assertEqual(response.status_code, code)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
