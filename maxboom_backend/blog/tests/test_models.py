import shutil
import tempfile

from django.test import override_settings, TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from blog.models import Post, Category, Tag


MEDIA_ROOT = tempfile.mkdtemp()

User = get_user_model()


class CategoryModelTest(TestCase):
    """
    Тестирование модели категорий.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            title='Тестовая категория',
            slug='test-category',
            meta_title='Мета-заголовок категории',
            meta_description='Мета-описание категории')

    def test_model_have_correct_object_name(self):
        """
        Тестирование корректности
        отображения __str__ у модели.
        """

        category = CategoryModelTest.category
        expected_category_name = category.title[:15]
        self.assertEqual(expected_category_name, str(category))

    def test_model_verbose_name(self):
        """
        verbose_name в полях совпадает с ожидаемым.
        """

        category = CategoryModelTest.category
        field_verboses = {
            'title': 'Название категории',
            'slug': 'Слаг',
            'meta_title': 'Мета-название страницы',
            'meta_description': 'Мета-описание страницы'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    category._meta.get_field(
                        field).verbose_name, expected_value)

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


class TagModelTest(TestCase):
    """
    Тестирование модели тегов.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag = Tag.objects.create(
            name='Тестовый тег'
            )

    def test_model_have_correct_object_name(self):
        """
        Тестирование корректности
        отображения __str__ у модели.
        """

        tag = TagModelTest.tag
        expected_tag_name = tag.name[:15]
        self.assertEqual(expected_tag_name, str(tag))

    def test_model_verbose_name(self):
        """
        verbose_name в полях совпадает с ожидаемым.
        """

        tag = TagModelTest.tag
        field_verboses = {
            'name': 'Название',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    tag._meta.get_field(
                        field).verbose_name, expected_value)

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class PostModelTest(TestCase):
    """
    Тестирование модели постов.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            title='Тестовая категория',
            slug='test-category-1',
            meta_title='Мета-заголовок категории',
            meta_description='Мета-описание категории')
        cls.tag = Tag.objects.create(
            name='Тестовый тег')
        cls.admin = User.objects.create_superuser(
            'admin@admin.com', 'adminpassword')
        cls.post = Post.objects.create(
            title='Первый тестовый пост',
            text='Текст для первого поста',
            author=cls.admin,
            image=SimpleUploadedFile(
                'test.jpg', b'something'),
            category=cls.category,
            slug='test-post',
            meta_title='Мета-заголовок поста',
            meta_description='Мета-описание поста')
        cls.post.tags.add(cls.tag)

    def test_model_have_correct_object_name(self):
        """
        Тестирование корректности
        отображения __str__ у модели.
        """

        post = PostModelTest.post
        expected_post_name = post.title[:30]
        self.assertEqual(expected_post_name, str(post))

    def test_model_verbose_name(self):
        """
        verbose_name в полях совпадает с ожидаемым.
        """

        post = PostModelTest.post
        field_verboses = {
            'title': 'Заголовок',
            'text': 'Текст',
            'author': 'Автор',
            'pub_date': 'Дата публикации',
            'image': 'Изображение',
            'category': 'Категория',
            'tags': 'Теги',
            'slug': 'Слаг',
            'meta_title': 'Мета-название страницы',
            'meta_description': 'Мета-описание страницы'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(
                        field).verbose_name, expected_value)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
