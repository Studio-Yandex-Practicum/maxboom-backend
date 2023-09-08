from django.test import TestCase
from shop_reviews.models import ShopReviews, ReplayToReview


class ShopReviewsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.review = ShopReviews.objects.create(
            text='Тестовый текст',
            author_name='Василий Петрович',
            author_email='vasil_test@mail.ru',
            delivery_speed_score=4,
            quality_score=3,
            price_score=3
        )

    def test_models_have_correct_object_name(self):
        review = ShopReviewsModelTest.review
        expected_review_name = review.text[:15]
        self.assertEqual(
            expected_review_name, str(review)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        review = ShopReviewsModelTest.review
        field_verboses = {
            'text': 'Отзыв',
            'pub_date': 'Дата создания отзыва',
            'author_name': 'Имя',
            'author_email': 'Почта',
            'delivery_speed_score': 'Скорость доставки',
            'quality_score': 'Качество товара',
            'price_score': 'Цена',
            'is_published': 'Публикация',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    review._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        review = ShopReviewsModelTest.review
        field_help_texts = {
            'text': 'Отзыв о магазине',
            'pub_date': 'Дата создания отзыва',
            'author_name': 'Имя автора отзыва',
            'author_email': 'Почта автора отзыва',
            'delivery_speed_score': 'Оценка скорости доставки товаров',
            'quality_score': 'Оценка качества товара в магазине',
            'price_score': 'Оценка цен в магазине',
            'is_published': 'Разрешить публикацию отзыва',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    review._meta.get_field(field).help_text, expected_value)

    def test_get_average_score(self):
        review = ShopReviewsModelTest.review
        scores = [review.delivery_speed_score,
                  review.price_score, review.quality_score]
        expected_scores_avg = round(sum(scores)/len(scores), 1)
        self.assertEqual(
            expected_scores_avg, review.average_score
        )

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


class ReplayToReviewModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.review = ShopReviews.objects.create(
            text='Тестовый отзыв',
            author_name='Василий Петрович',
            author_email='vasil_test@mail.ru',
            delivery_speed_score=4,
            quality_score=3,
            price_score=3
        )
        cls.replay = ReplayToReview.objects.create(
            text='Тестовый ответ',
            review_id=ReplayToReviewModelTest.review
        )

    def test_models_have_correct_object_name(self):
        replay = ReplayToReviewModelTest.replay
        expected_replay_name = replay.text[:15]
        self.assertEqual(
            expected_replay_name, str(replay)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        replay = ReplayToReviewModelTest.replay
        field_verboses = {
            'text': 'Ответ',
            'name': 'Имя',
            'pub_date': 'Дата',
            'review_id': 'Отзыв о магазине'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    replay._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        replay = ReplayToReviewModelTest.replay
        field_help_texts = {
            'text': 'Ответ на отзыв',
            'name': 'Имя автора ответа',
            'pub_date': 'Дата создания ответа',
            'review_id': 'Отзыв о магазине, на который отвечает администратор'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    replay._meta.get_field(field).help_text, expected_value)

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
