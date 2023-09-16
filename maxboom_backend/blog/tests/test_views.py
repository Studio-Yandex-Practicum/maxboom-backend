import shutil
import tempfile

from django.test import override_settings, TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from blog.models import Post, Category, Tag


MEDIA_ROOT = tempfile.mkdtemp()

User = get_user_model()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class NewsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Создание поста, категории, тега и админа
        для всего тестирования.
        """

        super().setUpClass()
        cls.admin = User.objects.create_superuser(
            'admin@admin.com', 'adminpassword')
        cls.category = Category.objects.create(
            title='Тестовая категория',
            slug='test-category')
        cls.tag = Tag.objects.create(
            name='Тестовый тег')
        cls.post = Post.objects.create(
            title='Тестовый пост',
            text='Текст для тестов',
            author=User.objects.filter(
                email='admin@admin.com').first(),
            image=SimpleUploadedFile(
                'test.jpg', b'something'),
            category=Category.objects.filter(
                title='Тестовая категория').first(),
            slug='test-slug')
        cls.post.tags.add(cls.tag)

    @classmethod
    def tearDownClass(cls):
        """
        Удаление временной папки для медиа после всех тестов.
        """

        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_posts_list_unauthenticated(self):
        """
        Получение списка всех постов
        для неавторизованных пользователей.
        """

        response = self.client.get(
            '/api/shopblog/posts/')
        post_instance = Post.objects.first()
        tag_instance = Tag.objects.first()
        url_image = 'http://testserver/media/' + str(post_instance.image)
        pub_date = post_instance.pub_date.strftime('%Y-%m-%d')
        expected_data = {
            'id': post_instance.pk,
            'title': post_instance.title,
            'text': post_instance.text,
            'image': url_image,
            'pub_date': pub_date,
            'author': 'Администратор',
            'category': post_instance.category.title,
            'tags': tag_instance.name,
            'slug': post_instance.slug
        }
        for key, expected_value in expected_data.items():
            with self.subTest(key=key):
                if key != 'category' and key != 'tags':
                    self.assertEqual(
                        response.data.get('results')[0].get(key),
                        expected_value)
                elif key == 'category':
                    self.assertEqual(
                        response.data.get(
                            "results")[0].get(key).get("title"), expected_value
                    )
                elif key == 'tags':
                    self.assertEqual(
                        response.data.get(
                            "results")[0].get(key)[0].get(
                                "name"), expected_value
                    )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
