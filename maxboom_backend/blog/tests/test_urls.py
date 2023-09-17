from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Post, Category


User = get_user_model()


class BlogUrlTests(TestCase):
    """
    Тестирование эндпоинтов приложения blog.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = User.objects.create_superuser(
            'admin@admin.com', 'adminpassword')
        cls.category = Category.objects.create(
            title='Тестовая категория',
            slug='test-category-1',
            meta_title='Мета-заголовок категории',
            meta_description='Мета-описание категории')
        cls.post = Post.objects.create(
            title='Тестовый пост',
            text='Текст для поста',
            author=cls.admin,
            category=cls.category,
            slug='test-post',
            meta_title='Мета-заголовок поста',
            meta_description='Мета-описание поста')

    def setUp(self):
        self.user_client = APIClient()

    def test_blog_urls_for_unauthenticated(self):
        """
        Тестирование доступа к эндпоинтам приложения blog
        для неавторизованных пользователей.
        """

        category = BlogUrlTests.category
        post = BlogUrlTests.post
        pages_statuses = {
            '/api/': status.HTTP_200_OK,
            '/api/shopblog/': status.HTTP_200_OK,
            '/api/shopblog/categories/': status.HTTP_200_OK,
            f'/api/shopblog/categories/{category.slug}/': status.HTTP_200_OK,
            '/api/shopblog/posts/': status.HTTP_200_OK,
            f'/api/shopblog/posts/{post.slug}/': status.HTTP_200_OK,
        }
        for url, code in pages_statuses.items():
            with self.subTest(url=url):
                response = self.user_client.get(url)
                self.assertEqual(response.status_code, code)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
