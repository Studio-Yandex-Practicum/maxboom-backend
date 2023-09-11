from http import HTTPStatus
from django.test import TestCase
from rest_framework.test import APIClient
from shop_reviews.models import ShopReviews, ReplayToReview
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


class ShopReviewsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            review_id=ShopReviewsURLTests.review
        )
        cls.admin = User.objects.create_superuser(
            'admin@example.com', 'admin')

    def setUp(self):
        self.user_client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.force_login(ShopReviewsURLTests.admin)

    def test_user_get_urls(self):
        """доступные пользователям url"""
        review = ShopReviewsURLTests.review
        replay = ShopReviewsURLTests.replay
        status_pages = {
            '/api/': HTTPStatus.OK,
            '/api/store-reviews/': HTTPStatus.OK,
            f'/api/store-reviews/{review.pk}/': HTTPStatus.OK,
            f'/api/store-reviews/{review.pk}/replay/': HTTPStatus.UNAUTHORIZED,  #cHTTPStatus.FORBIDDEN,
            '/api/store-reviews/'
            f'{review.pk}/replay/{replay.pk}/': HTTPStatus.UNAUTHORIZED, # HTTPStatus.FORBIDDEN,
            '/unexisting_page': HTTPStatus.NOT_FOUND
        }
        for address, code in status_pages.items():
            with self.subTest(address=address):
                response = self.user_client.get(address)
                self.assertEqual(response.status_code, code, f'{address}')

    def test_admin_get_urls(self):
        """доступные администратору url"""
        review = ShopReviewsURLTests.review
        replay = ShopReviewsURLTests.replay
        status_pages = {
            '/api/': HTTPStatus.OK,
            '/api/store-reviews/': HTTPStatus.OK,
            f'/api/store-reviews/{review.pk}/': HTTPStatus.OK,
            f'/api/store-reviews/{review.pk}/replay/': HTTPStatus.OK,
            '/api/store-reviews/'
            f'{review.pk}/replay/{replay.pk}/': HTTPStatus.OK,
            '/unexisting_page': HTTPStatus.NOT_FOUND
        }
        for address, code in status_pages.items():
            with self.subTest(address=address):
                response = self.admin_client.get(address)
                self.assertEqual(response.status_code, code, f'{address}')

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
