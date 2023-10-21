from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from shop_reviews.models import ReplayToReview, ShopReviews

User = get_user_model()


class ShopReviewsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.review_new = ShopReviews.objects.create(
            text='Новый тестовый текст',
            author_name='Василий Иванович',
            author_email='Ivan_test@mail.ru',
            delivery_speed_score=4,
            quality_score=3,
            price_score=3,
            is_published=True
        )
        cls.admin = User.objects.create_superuser(
            'admin1@example.com', 'admin1')
        cls.review = ShopReviews.objects.create(
            text='Тестовый текст',
            author_name='Василий Петрович',
            author_email='vasil_test@mail.ru',
            delivery_speed_score=4,
            quality_score=3,
            price_score=3,
            is_published=True
        )
        cls.replay = ReplayToReview.objects.create(
            text='Тестовый ответ',
            review_id=cls.review
        )

    def setUp(self):
        self.user_client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.force_login(ShopReviewsViewTests.admin)

    def test_user_post_review(self):
        """создание отзыва пользователем"""
        address = '/api/store-reviews/'
        reviews_count_expected = ShopReviews.objects.count() + 1
        data = {
            'text': 'Тестовый текст12',
            'author_name': 'Василий Петрович1',
            'author_email': 'vasil_test1@mail.ru',
            'delivery_speed_score': 5,
            'quality_score': 3,
            'price_score': 3,
            'is_published': True
        }
        response = self.user_client.post(address, data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED,
                         'Отзыв не создан')
        reviews_count = ShopReviews.objects.count()
        self.assertEqual(reviews_count_expected, reviews_count,
                         'Количество отзывов не совпало')
        last_review = ShopReviews.objects.get(text='Тестовый текст12')
        self.assertEqual(last_review.is_published, False,
                         'Пользователь не должен публиковать отзывы')
        expected_review = {
            'text': 'Тестовый текст12',
            'author_name': 'Василий Петрович1',
            'author_email': 'vasil_test1@mail.ru',
            'delivery_speed_score': 5,
            'quality_score': 3,
            'price_score': 3,
            'replay': None,
            'average_score': 3.7
        }
        for key, expected_value in expected_review.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key), expected_value, f'{key}')

    def test_user_put_review(self):
        """замена отзыва пользователем"""
        reviews = ShopReviews.objects.all().filter(
            is_published=True)[0]
        address = f'/api/store-reviews/{reviews.pk}/'
        data = {
            'text': 'Тестовый текст12',
            'author_name': 'Василий Петрович1',
            'author_email': 'vasil_test1@mail.ru',
            'delivery_speed_score': 5,
            'quality_score': 3,
            'price_score': 3,
            'is_published': True
        }
        response = self.user_client.put(address, data=data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED,
                         'Отзыв не заменяется')

    def test_user_patch_review(self):
        """редактирование отзыва пользователем"""
        reviews = ShopReviews.objects.filter(
            is_published=True)[0]
        address = f'/api/store-reviews/{reviews.pk}/'
        data = {
            'text': 'Тестовый текст13',
        }
        response = self.user_client.patch(address, data=data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED,
                         'Отзыв не редактируется')

    def test_user_get_list_is_published_review(self):
        """получение отзывов пользователем"""
        address = '/api/store-reviews/'
        reviews_count_expected = ShopReviews.objects.filter(
            is_published=True).count()
        response = self.user_client.get(address)
        reviews_count = len(response.data.get('results'))

        self.assertEqual(reviews_count_expected, reviews_count,
                         'Пользователь получил отзывы'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'pk': 2,
                'text': 'Тестовый текст',
                'author_name': 'Василий Петрович',
                'author_email': 'vasil_test@mail.ru',
                'average_score': 3.3,
                'delivery_speed_score': 4,
                'quality_score': 3,
                'price_score': 3,
                'replay': {
                    'text': 'Тестовый ответ',
                    'name': 'Администратор'
                }
            },
            {
                'pk': 1,
                'text': 'Новый тестовый текст',
                'author_name': 'Василий Иванович',
                'author_email': 'Ivan_test@mail.ru',
                'average_score': 3.3,
                'delivery_speed_score': 4,
                'quality_score': 3,
                'price_score': 3,
                'replay': None
            },

        ]
        self.check_fields(response=response.data.get(
            'results'), expected_data=expected_data)

    def check_fields(self, response, expected_data):
        if type(expected_data) is list and expected_data:
            for i in range(len(expected_data)):
                self.check_fields(
                    response=response[i], expected_data=expected_data[i])
        elif type(expected_data) is str:
            with self.subTest():
                self.assertEqual(
                    response,
                    expected_data,
                )
        else:
            for key, expected_value in expected_data.items():
                if type(expected_value) is list and expected_value:
                    for j in range(len(expected_value)):
                        self.check_fields(response=response.get(
                            key)[j], expected_data=expected_value[j])
                else:
                    if type(expected_value) is dict and expected_value:
                        self.check_fields(response=response.get(
                            key), expected_data=expected_value)
                    else:
                        with self.subTest(key=key):
                            self.assertEqual(
                                response.get(key),
                                expected_value,
                                f'{key}'
                            )

    def test_user_get_item_is_published_review(self):
        """получение отзыва пользователем"""
        reviews_expected = ShopReviewsViewTests.review
        address = f'/api/store-reviews/{reviews_expected.pk}/'
        response = self.user_client.get(address)
        expected_review = {
            'text': 'Тестовый текст',
            'author_name': 'Василий Петрович',
            'author_email': 'vasil_test@mail.ru',
            'delivery_speed_score': 4,
            'quality_score': 3,
            'price_score': 3,
            'average_score': 3.3
        }
        expected_review_replay = {
            'text': 'Тестовый ответ',
            'name': 'Администратор'
        }
        for key, expected_value in expected_review.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key),
                    expected_value,
                    f'{key}'
                )
        for key, expected_value in expected_review_replay.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get('replay').get(key),
                    expected_value,
                    f'{key}'
                )

    def test_admin_get_is_unpublished_review(self):
        """получение отзыва администратором"""
        address = '/api/store-reviews/'
        reviews_count_expected = ShopReviews.objects.all().count()
        response = self.admin_client.get(address)
        reviews_count = len(response.data.get('results'))

        self.assertEqual(reviews_count_expected, reviews_count,
                         'Администратор получил не все отзывы')

    def test_admin_post_review(self):
        """создание отзыва администратором"""
        address = '/api/store-reviews/'
        reviews_count_expected = ShopReviews.objects.count() + 1
        data = {
            'text': 'Тестовый текст12',
            'author_name': 'Василий Петрович1',
            'author_email': 'vasil_test1@mail.ru',
            'delivery_speed_score': 5,
            'quality_score': 3,
            'price_score': 3,
            'is_published': True
        }
        response = self.admin_client.post(address, data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED,
                         'Отзыв не создан')
        reviews_count = ShopReviews.objects.count()
        self.assertEqual(reviews_count_expected, reviews_count,
                         'Количество отзывов не совпало')
        last_review = ShopReviews.objects.get(text='Тестовый текст12')
        self.assertEqual(last_review.is_published, True,
                         'Администратор может публиковать отзывы')
        expected_review = {
            'text': 'Тестовый текст12',
            'author_name': 'Василий Петрович1',
            'author_email': 'vasil_test1@mail.ru',
            'delivery_speed_score': 5,
            'quality_score': 3,
            'price_score': 3,
            'replay': None,
            'average_score': 3.7,
            'is_published': True
        }
        for key, expected_value in expected_review.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key), expected_value, f'{key}')

    def test_admin_patch_review(self):
        """редактирование отзыва администратором"""
        review = ShopReviews.objects.all().filter(
            is_published=True)[0]
        address = f'/api/store-reviews/{review.pk}/'
        data = {'is_published': False}
        response = self.admin_client.patch(address, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'Отзыв не изменен')
        for key, expected_value in data.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key),
                    expected_value,
                    f'{key}'
                )

    def test_admin_put_review(self):
        review = ShopReviews.objects.all().filter(
            is_published=True)[0]
        address = f'/api/store-reviews/{review.pk}/'
        data = {
            'text': 'Тестовый текст12',
            'author_name': 'Василий Петрович1',
            'author_email': 'vasil_test1@mail.ru',
            'delivery_speed_score': 5,
            'quality_score': 3,
            'price_score': 3,
            'is_published': True
        }
        response = self.admin_client.put(address, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'Отзыв не изменен')
        expected_review = {
            'text': 'Тестовый текст12',
            'author_name': 'Василий Петрович1',
            'author_email': 'vasil_test1@mail.ru',
            'delivery_speed_score': 5,
            'quality_score': 3,
            'price_score': 3,
            'average_score': 3.7
        }
        for key, expected_value in expected_review.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key), expected_value, f'{key}')

    def test_admin_get_replay_list(self):
        """Получение ответа на отзыв администратором"""
        review = ShopReviewsViewTests.review
        address = f'/api/store-reviews/{review.pk}/replay/'
        response = self.admin_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'Ответ не получен')
        expected_replay = {
            'text': 'Тестовый ответ',
            'name': 'Администратор'
        }
        for key, expected_value in expected_replay.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data[0].get(key), expected_value, f'{key}')

    def test_admin_get_replay_item(self):
        """Получение ответа на отзыв администратором"""
        replay = ReplayToReview.objects.all()[0]
        address = ('/api/store-reviews/'
                   f'{replay.review_id.pk}'
                   f'/replay/{replay.pk}/'
                   )
        response = self.admin_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'Ответ не получен')
        expected_replay = {
            'text': 'Тестовый ответ',
            'name': 'Администратор'
        }
        for key, expected_value in expected_replay.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key), expected_value, f'{key}')

    def test_admin_post_replay(self):
        """создание ответа на отзыв администратором"""
        review = ShopReviews.objects.filter(replay=None)[0]
        replay_count_expected = ReplayToReview.objects.count() + 1
        address = f'/api/store-reviews/{review.pk}/replay/'
        data = {"text": "Спасибо."}
        response = self.admin_client.post(address, data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED,
                         'Ответ на отзыв не создан')
        replay_count = ReplayToReview.objects.count()
        self.assertEqual(replay_count_expected, replay_count,
                         'Не увеличилось количество ответов в базе')
        for key, expected_value in data.items():
            with self.subTest(key=key):
                self.assertEqual(
                    response.data.get(key), expected_value, f'{key}')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
