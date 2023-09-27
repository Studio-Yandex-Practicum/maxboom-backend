import shutil
import tempfile

from django.test import override_settings, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from news.models import News


MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class NewsModelTest(TestCase):
    """
    Тестирование модели новостей.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.news = News.objects.create(
            title='Заголовок для тестов',
            text='Текст для тестов',
            image=SimpleUploadedFile(
                'test.jpg', b'something'),
            slug='test-slug',
            meta_title='Мета-заголовок новости',
            meta_description='Мета-описание новости')

    def test_model_have_correct_object_name(self):
        """
        Тестирование корректности
        отображения __str__ у модели.
        """

        news = NewsModelTest.news
        expected_category_name = news.title[:30]
        self.assertEqual(expected_category_name, str(news))

    def test_model_verbose_name(self):
        """
        verbose_name в полях совпадает с ожидаемым.
        """

        news = NewsModelTest.news
        field_verboses = {
            'title': 'Заголовок',
            'text': 'Текст',
            'image': 'Изображение',
            'pub_date': 'Дата публикации',
            'slug': 'Слаг',
            'meta_title': 'Мета-название страницы',
            'meta_description': 'Мета-описание страницы'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    news._meta.get_field(
                        field).verbose_name, expected_value)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
