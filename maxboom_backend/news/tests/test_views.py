import shutil
import tempfile

from django.test import override_settings, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from news.models import News


MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class NewsViewTests(TestCase):
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
            slug='test-slug'
        )

    @classmethod
    def tearDownClass(cls):
        """
        Удаление временной папки для медиа после всех тестов.
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_list_unauthenticated(self):
        """
        Получение списка всех новостей
        для неавторизованных пользователей.
        """
        response = self.client.get(
            '/api/shopnews/')
        instance = News.objects.first()
        url_image = 'http://testserver/media/' + str(instance.image)
        pub_date = instance.pub_date.strftime('%Y-%m-%d')
        expected_data = {
            'id': instance.pk,
            'title': instance.title,
            'text': instance.text,
            'image': url_image,
            'pub_date': pub_date,
            'slug': instance.slug
        }
        for key, expected_value in expected_data.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get('results')[0].get(key),
                    expected_value)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_unauthenticated(self):
        """
        Получение новости по {pk}
        для неавторизованных пользователей.
        """
        instance = News.objects.first()
        response = self.client.get(
            f'/api/shopnews/{instance.slug}/')
        url_image = 'http://testserver/media/' + str(instance.image)
        pub_date = instance.pub_date.strftime('%Y-%m-%d')
        expected_data = {
            'id': instance.pk,
            'title': instance.title,
            'text': instance.text,
            'image': url_image,
            'pub_date': pub_date,
            'slug': instance.slug
        }
        for key, expected_value in expected_data.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key),
                    expected_value)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
