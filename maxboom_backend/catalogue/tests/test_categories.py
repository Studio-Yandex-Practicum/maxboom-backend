from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from catalogue.models import Category


class CategoryViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email='test@mail.com',
            password='test_password',
            is_staff=True,
        )
        cls.category = Category.objects.create(
            name='Категория',
            slug='category',
            meta_title='мета-название',
            meta_description='мета-писание',
        )

        cls.url = reverse('category-list')

    def test_request_from_unauthorized(self):
        '''Get-запрос к категориям доступен неавторизованному юзеру.'''
        response = self.client.get(CategoryViewTest.url)

        self.assertEqual(
            response.status_code,
            200,
            'Эндпоинт должен быть доступен авторизованному юзеру.',
        )

    def test_get_request_correct_response(self):
        '''Эндпоинт категорий возвращает корректные данные при get-запросе.'''
        response = self.client.get(CategoryViewTest.url)
        correct_data = {
            'id': CategoryViewTest.category.id,
            'name': CategoryViewTest.category.name,
            'slug': CategoryViewTest.category.slug,
            'meta_title': CategoryViewTest.category.meta_title,
            'meta_description': CategoryViewTest.category.meta_description,
        }

        self.assertEqual(
            len(response.data['results']),
            1,
            'Вернулось неверное количество категорий.',
        )
        for field, value in correct_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    response.data['results'][0][field],
                    value,
                    f'Вернулось неверное значение поля {field}',
                )

    def test_post_request_from_unauthorized(self):
        '''Post-запрос к категориям недоступен неавторизованному юзеру.'''
        response = self.client.post(
            CategoryViewTest.url,
            data={
                'name': 'Категория2',
                'slug': 'category_2',
                'meta_title': 'Название2',
                'meta_description': 'Описание2',
            },
        )

        self.assertEqual(
            response.status_code,
            401,
            'Post-запрос должен быть недоступен для анонима.',
        )

    def test_post_request_correct_data(self):
        '''Категория создается с корректными данными при post-запросе.'''
        categories_count = Category.objects.count()
        self.client.force_authenticate(CategoryViewTest.user)
        response = self.client.post(
            CategoryViewTest.url,
            data={
                'name': 'Категория3',
                'slug': 'category_3',
                'meta_title': 'Название3',
                'meta_description': 'Описание3',
            },
        )

        self.assertEqual(
            Category.objects.count(),
            categories_count + 1,
            'Категория не создалась в базе данных.',
        )
        self.assertEqual(
            response.status_code,
            201,
            'Post-запрос должен быть недоступен для анонима.',
        )
        new_category = Category.objects.get(name='Категория3')
        self.assertEqual(
            new_category.meta_title,
            'Название3',
            'Категория создается с неверным мета-названием',
        )
        self.assertEqual(
            new_category.meta_description,
            'Описание3',
            'Категория создается с неверным мета-описанием',
        )

    def test_create_category_name_already_exists(self):
        '''Невозможно создать категорию с названием, которое уже занято.'''
        categories_count = Category.objects.count()
        self.client.force_authenticate(CategoryViewTest.user)
        response = self.client.post(
            CategoryViewTest.url,
            data={
                'name': 'Категория',
                'slug': 'category',
                'meta_title': 'Название',
                'meta_description': 'Описание',
            },
        )

        self.assertEqual(
            Category.objects.count(),
            categories_count,
            'Категория не должна создаться в БД.',
        )
        self.assertEqual(
            response.status_code,
            400,
            'Вернулся неверный код ответа.',
        )

    def test_update_request_from_unauthorized(self):
        '''PUT и PATCH-запросы недоступны для неавторизованного юзера.'''
        response = self.client.put(
            f'{CategoryViewTest.url}1/',
            data={
                'name': 'Новое',
                'slug': 'category',
                'meta_title': 'Новое мета-название',
                'meta_description': 'Новое мета-описание',
            },
        )

        self.assertEqual(
            response.status_code,
            401,
            'Update-запрос должен быть недоступен для анонима.',
        )

    def test_update_request_correct_data(self):
        '''При Update-запросе данные категории корректно обновляются.'''
        new_category = Category.objects.create(
            name='Название',
            meta_title='мета-название',
            meta_description='мета-писание',
        )
        put_data = {
            'name': 'Новое название',
            'slug': 'new_category',
            'meta_title': 'Новое мета-название',
            'meta_description': 'Новое мета-описание',
        }
        self.client.force_authenticate(CategoryViewTest.user)
        response = self.client.put(
            f'{CategoryViewTest.url}{new_category.id}/', data=put_data
        )

        self.assertEqual(
            response.status_code,
            200,
            'Вернулся неверный код ответа.',
        )

        updated_category = Category.objects.get(id=new_category.id)

        for field in ('name', 'meta_title', 'meta_description'):
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(updated_category, field),
                    put_data[field],
                    f'Неверно обновилось поле {field}',
                )

    def test_delete_request_from_unauthorized(self):
        '''Delete-запрос к категориям недоступен неавторизованному юзеру.'''
        categories_count = Category.objects.count()
        response = self.client.delete(f'{CategoryViewTest.url}1/')

        self.assertEqual(
            response.status_code,
            401,
            'Delete-запрос должен быть недоступен для анонима.',
        )
        self.assertEqual(
            Category.objects.count(),
            categories_count,
            'Категория не должна создаться в БД.',
        )

    def test_delete_request_from_admin(self):
        '''При delete-запросе категорий удаляется из БД.'''
        new_category = Category.objects.create(
            name='Категория для удаления',
            meta_title='мета-название',
            meta_description='мета-писание',
        )
        categories_count = Category.objects.count()
        self.client.force_authenticate(CategoryViewTest.user)
        response = self.client.delete(
            f'{CategoryViewTest.url}{new_category.id}/'
        )

        self.assertEqual(
            response.status_code,
            204,
            'Delete-запрос должен быть доступен для админа.',
        )
        self.assertEqual(
            Category.objects.count(),
            categories_count - 1,
            'Категория должна удаляться из БД.',
        )

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
