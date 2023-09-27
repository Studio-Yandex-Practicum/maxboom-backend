import shutil
import tempfile

from django.test import override_settings, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from news.models import News


MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class NewsViewTests(TestCase):
    """
    Тестирование возвращаемого ответа по эндпоинтам
    приложения news.
    """

    @classmethod
    def setUpClass(cls):
        """
        Создание новости для всего тестирования.
        """

        super().setUpClass()
        cls.news = News.objects.create(
            title='Заголовок для тестов',
            text='Текст для тестов',
            image=SimpleUploadedFile(
                'test.jpg', b'something'),
            slug='test-slug',
            meta_title='Мета-заголовок новости',
            meta_description='Мета-описание новости')

    def setUp(self):
        super().setUp()
        self.user_client = APIClient()

    def test_category_list_unauthenticated(self):
        """
        Получение списка всех новостей
        для неавторизованных пользователей.
        """

        news = NewsViewTests.news
        url_image = 'http://testserver/media/' + str(news.image)
        pub_date = news.pub_date.strftime('%Y-%m-%d')
        expected_data = {
            'id': news.id,
            'title': 'Заголовок для тестов',
            'text': 'Текст для тестов',
            'image': url_image,
            'pub_date': pub_date,
            'slug': 'test-slug'
        }
        response = self.user_client.get(
            '/api/shopnews/')
        for key, expected_value in expected_data.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get('results')[0].get(key),
                    expected_value)
        self.assertEqual(
            len(response.data['results']), News.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_unauthenticated(self):
        """
        Получение новости по {slug}
        для неавторизованных пользователей.
        """

        news = NewsViewTests.news
        url_image = 'http://testserver/media/' + str(news.image)
        pub_date = news.pub_date.strftime('%Y-%m-%d')
        expected_data = {
            'id': news.id,
            'title': 'Заголовок для тестов',
            'text': 'Текст для тестов',
            'image': url_image,
            'pub_date': pub_date,
            'slug': 'test-slug'
        }
        response = self.user_client.get(
            f'/api/shopnews/{news.slug}/')
        for key, expected_value in expected_data.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key),
                    expected_value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
