import shutil
import tempfile

from django.test import override_settings, TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Post, Category, Tag, Comments


MEDIA_ROOT = tempfile.mkdtemp()

User = get_user_model()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class BlogViewTests(TestCase):
    """
    Тестирование возвращаемого ответа по эндпоинтам
    приложения blog.
    """

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """
        Создание постов, категории, тегов и админа
        для всего тестирования.
        """

        super().setUpClass()
        cls.admin = User.objects.create_superuser(
            'admin@admin.com', 'adminpassword')
        cls.category_1 = Category.objects.create(
            title='Первая тестовая категория',
            slug='test-category-1',
            meta_title='Мета-заголовок первой категории',
            meta_description='Мета-описание первой категории')
        cls.category_2 = Category.objects.create(
            title='Вторая тестовая категория',
            slug='test-category-2',
            meta_title='Мета-заголовок второй категории',
            meta_description='Мета-описание второй категории')
        cls.tag_1 = Tag.objects.create(
            name='Тестовый тег 1')
        cls.tag_2 = Tag.objects.create(
            name='Тестовый тег 2')
        cls.post_1 = Post.objects.create(
            title='Первый тестовый пост',
            text='Текст для первого поста',
            author=cls.admin,
            image=SimpleUploadedFile(
                'test_1.jpg', b'something_1'),
            category=cls.category_1,
            slug='first-post',
            meta_title='Мета-заголовок первого поста',
            meta_description='Мета-описание первого поста')
        cls.post_1.tags.add(cls.tag_1, cls.tag_2)
        cls.post_2 = Post.objects.create(
            title='Второй тестовый пост',
            text='Текст для второго поста',
            image=SimpleUploadedFile(
                'test_2.jpg', b'something_2'),
            category=cls.category_2,
            slug='second-post',
            meta_title='Мета-заголовок второго поста',
            meta_description='Мета-описание второго поста')
        cls.post_2.tags.add(cls.tag_1)
        cls.comment_1 = Comments.objects.create(
            author='Тестовый пользователь 1',
            post=cls.post_1,
            text='Первый тестовый комментарий',
            is_published=True)
        cls.comment_2 = Comments.objects.create(
            author='Тестовый пользователь 2',
            post=cls.post_1,
            text='Второй тестовый комментарий',
            is_published=False)

    def setUp(self):
        super().setUp()
        self.user_client = APIClient()

    def test_posts_list_unauthenticated(self):
        """
        Получение списка всех постов
        для неавторизованных пользователей.
        """

        id_post_1 = BlogViewTests.post_1.id
        url_image_post_1 = 'http://testserver/media/' + str(
            BlogViewTests.post_1.image)
        pub_date_post_1 = BlogViewTests.post_1.pub_date.strftime('%Y-%m-%d')
        views_post_1 = BlogViewTests.post_1.views
        expected_data_post_1 = {
            'id': id_post_1,
            'title': 'Первый тестовый пост',
            'text': 'Текст для первого поста',
            'pub_date': pub_date_post_1,
            'author': 'Администратор',
            'image': url_image_post_1,
            'category': {
                'title': 'Первая тестовая категория',
                'slug': 'test-category-1'
            },
            'tags': [
                {
                    'name': 'Тестовый тег 1'
                },
                {
                    'name': 'Тестовый тег 2'
                }
            ],
            'views': views_post_1,
            'slug': 'first-post',
            'meta_title': 'Мета-заголовок первого поста',
            'meta_description': 'Мета-описание первого поста'
        }
        url = '/api/shopblog/posts/'
        response = self.user_client.get(url)
        response_data_post_1 = response.data['results'][0]
        for key, value in expected_data_post_1.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(response_data_post_1[key], value)
        self.assertEqual(
            len(response.data['results']), Post.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_posts_retrieve_unauthenticated(self):
        """
        Получение поста по {slug}
        для неавторизованных пользователей.
        """

        id_post_1 = BlogViewTests.post_1.id
        url_image_post_1 = 'http://testserver/media/' + str(
            BlogViewTests.post_1.image)
        pub_date_post_1 = BlogViewTests.post_1.pub_date.strftime('%Y-%m-%d')
        views_post_1 = BlogViewTests.post_1.views
        slug_post_1 = BlogViewTests.post_1.slug
        expected_data_post_1 = {
            'id': id_post_1,
            'title': 'Первый тестовый пост',
            'text': 'Текст для первого поста',
            'pub_date': pub_date_post_1,
            'author': 'Администратор',
            'image': url_image_post_1,
            'category': {
                'title': 'Первая тестовая категория',
                'slug': 'test-category-1'
            },
            'tags': [
                {
                    'name': 'Тестовый тег 1'
                },
                {
                    'name': 'Тестовый тег 2'
                }
            ],
            'views': views_post_1 + 1,
            'slug': 'first-post',
            'meta_title': 'Мета-заголовок первого поста',
            'meta_description': 'Мета-описание первого поста'
        }
        url = '/api/shopblog/posts'
        response = self.user_client.get(f'{url}/{slug_post_1}/')
        for key, value in expected_data_post_1.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(response.data[key], value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_list_unauthenticated(self):
        """
        Получение списка всех категорий
        для неавторизованных пользователей.
        """

        expected_data_category_1 = {
            'title': 'Первая тестовая категория',
            'slug': 'test-category-1',
            'meta_title': 'Мета-заголовок первой категории',
            'meta_description': 'Мета-описание первой категории'
        }
        url = '/api/shopblog/categories/'
        response = self.user_client.get(url)
        response_data_category_1 = response.data['results'][1]
        for key, value in expected_data_category_1.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(response_data_category_1[key], value)
        self.assertEqual(
            len(response.data['results']), Category.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_retrieve_unauthenticated(self):
        """
        Получение категории по {slug}
        для неавторизованных пользователей.
        """

        id_post_1 = BlogViewTests.post_1.id
        url_image_post_1 = 'http://testserver/media/' + str(
            BlogViewTests.post_1.image)
        pub_date_post_1 = BlogViewTests.post_1.pub_date.strftime('%Y-%m-%d')
        views_post_1 = BlogViewTests.post_1.views
        comments_quantity = Comments.objects.filter(
            post__id=id_post_1, is_published=True)
        slug_category_1 = BlogViewTests.category_1.slug
        expected_data_category_1 = {
            'title': 'Первая тестовая категория',
            'slug': 'test-category-1',
            'meta_title': 'Мета-заголовок первой категории',
            'meta_description': 'Мета-описание первой категории',
            'posts': [
                {
                    'id': id_post_1,
                    'title': 'Первый тестовый пост',
                    'text': 'Текст для первого поста',
                    'pub_date': pub_date_post_1,
                    'author': 'Администратор',
                    'image': url_image_post_1,
                    'tags': [
                        {
                            'name': 'Тестовый тег 1'
                        },
                        {
                            'name': 'Тестовый тег 2'
                        }
                    ],
                    'views': views_post_1,
                    'comments_quantity': comments_quantity.count(),
                    'slug': 'first-post'
                }
            ]
        }
        url = '/api/shopblog/categories'
        response = self.user_client.get(f'{url}/{slug_category_1}/')
        for key, value in expected_data_category_1.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(response.data[key], value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comments_list_unathenticated(self):
        """
        Получение списка всех опубликованных комментариев
        для неавторизованных пользователей.
        """

        id_comment_1 = BlogViewTests.comment_1.id
        pub_date_comment_1 = BlogViewTests.comment_1.pub_date.strftime(
            '%Y-%m-%d')
        slug_post_1 = BlogViewTests.post_1.slug
        expected_data_comment_1 = {
            'id': id_comment_1,
            'author': 'Тестовый пользователь 1',
            'text': 'Первый тестовый комментарий',
            'pub_date': pub_date_comment_1
        }
        url = f'/api/shopblog/posts/{slug_post_1}/comments/'
        response = self.user_client.get(url)
        response_data_comment_1 = response.data['results'][0]
        for key, value in expected_data_comment_1.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(response_data_comment_1[key], value)
        self.assertEqual(
            len(response.data['results']), Comments.objects.filter(
                is_published=True).count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comments_post_unathenticated(self):
        """
        Создание комментариев
        для неавторизованных пользователей.
        """

        slug_post_1 = BlogViewTests.post_1.slug
        url = f'/api/shopblog/posts/{slug_post_1}/comments/'
        comments = Comments.objects.filter(post=BlogViewTests.post_1,
                                           is_published=True)
        data = {
            'author': 'Тестовый пользователь',
            'text': 'Тестовый текст'
        }
        response_get_before_publish = self.client.get(url)
        response_add = self.user_client.post(url, data=data)
        self.assertEqual(response_add.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            len(response_get_before_publish.data['results']),
            comments.count())
        comment_added = Comments.objects.filter(id=3)[0]
        comment_added.is_published = True
        comment_added.save()
        response_get_after_publish = self.client.get(url)
        for key, value in data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(
                    response_get_after_publish.data['results'][1][key], value)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
