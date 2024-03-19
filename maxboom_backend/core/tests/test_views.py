# flake8: noqa
from http import HTTPStatus
import tempfile
import shutil

from django.conf import settings
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from core.models import (
    About, DeliveryInformation, Privacy, Terms,
    Contacts, Requisite, MainShop, OurShop,
    MailContactForm, MailContact, Header, Footer,
    MainLogo, AdditionalLogo, Support
)


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class InfoModelsViewsTest(TestCase):

    image_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    image = SimpleUploadedFile(
        'image_gif.gif',
        image_gif,
        content_type='image/gif'
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.about = About.objects.create(
            headline='Тест-заглавие "О нас"',
            text='Тест-текст "О нас',
            meta_title='Тест-мета-заглавие "О нас"',
            meta_description='Тест-мета-описание "О нас"'
        )
        cls.delivery = DeliveryInformation.objects.create(
            headline='Тест-заглавие "Доставка"',
            text='Тест-текст "Доставка',
            meta_title='Тест-мета-заглавие "Доставка"',
            meta_description='Тест-мета-описание "Доставка"'
        )
        cls.privacy = Privacy.objects.create(
            headline='Тест-заглавие "Политика"',
            text='Тест-текст "Политика',
            meta_title='Тест-мета-заглавие "Политика"',
            meta_description='Тест-мета-описание "Политика"'
        )
        cls.terms = Terms.objects.create(
            headline='Тест-заглавие "Условия"',
            text='Тест-текст "Условия',
            meta_title='Тест-мета-заглавие "Условия"',
            meta_description='Тест-мета-описание "Условия"'
        )
        cls.contacts = Contacts.objects.create(
            headline='Тест-заглавие "Контакты"',
            meta_title='Тест-мета-заглавие "Контакты"',
            meta_description='Тест-мета-описание "Контакты"'
        )
        cls.mail_form = MailContactForm.objects.create(
            headline='Тестовый заголовок формы',
            ask_name='Введите имя',
            ask_email='Введите e-mail',
            ask_message='Введите сообщение',
            send_button_text='Отправить',
            main_page=cls.contacts
        )
        cls.main_shop = MainShop.objects.create(
            name='Тестовый магазин на дворе',
            comment='Будни с 8:00 до 20:00',
            phone_number='1234567890',
            email='test@test.test',
            location='Тестовая локация',
            main_page=cls.contacts
        )
        cls.our_shop = OurShop.objects.create(
            name='Тестовый магазин за углом',
            comment='Будни с 20:00 до 8:00',
            phone_number='0987654321',
            photo=cls.image,
            is_main_shop=True,
            main_page=cls.contacts
        )
        cls.our_shop_2 = OurShop.objects.create(
            name='Тестовый магазин на дворе',
            comment='Будни с 8:00 до 20:00',
            phone_number='1234567890',
            photo=cls.image,
            is_main_shop=False,
            main_page=cls.contacts
        )
        cls.requisite = Requisite.objects.create(
            requisite_name='Тестовый реквизит',
            requisite_description='Тестовое описание',
            main_page=cls.contacts
        )
        cls.requisite_2 = Requisite.objects.create(
            requisite_name='Тестовый реквизит 2',
            requisite_description='Тестовое описание 2',
            main_page=cls.contacts
        )
        cls.superuser = User.objects.create_superuser(
            'test2@test.test', 'test'
        )

    def setUp(self):
        super().setUp()
        self.user_client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.force_login(InfoModelsViewsTest.superuser)

    def test_about_viewset(self):
        """Проверка эндпоинта about."""
        url = '/api/core/about/'
        expected_data = {
            'headline': 'Тест-заглавие "О нас"',
            'text': 'Тест-текст "О нас',
            'meta_title': 'Тест-мета-заглавие "О нас"',
            'meta_description': 'Тест-мета-описание "О нас"'
        }
        response = self.user_client.get(url)
        response_data = response.data[0]
        for key, value in expected_data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(
                    response_data[key], value
                )

    def test_delivery_viewset(self):
        """Проверка эндпоинта information."""
        url = '/api/core/information/'
        expected_data = {
            'headline': 'Тест-заглавие "Доставка"',
            'text': 'Тест-текст "Доставка',
            'meta_title': 'Тест-мета-заглавие "Доставка"',
            'meta_description': 'Тест-мета-описание "Доставка"'
        }
        response = self.user_client.get(url)
        response_data = response.data[0]
        for key, value in expected_data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(
                    response_data[key], value
                )

    def test_privacy_viewset(self):
        """Проверка эндпоинта privacy."""
        url = '/api/core/privacy/'
        expected_data = {
            'headline': 'Тест-заглавие "Политика"',
            'text': 'Тест-текст "Политика',
            'meta_title': 'Тест-мета-заглавие "Политика"',
            'meta_description': 'Тест-мета-описание "Политика"'
        }
        response = self.user_client.get(url)
        response_data = response.data[0]
        for key, value in expected_data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(
                    response_data[key], value
                )

    def test_terms_viewset(self):
        """Проверка эндпоинта terms."""
        url = '/api/core/terms/'
        expected_data = {
            'headline': 'Тест-заглавие "Условия"',
            'text': 'Тест-текст "Условия',
            'meta_title': 'Тест-мета-заглавие "Условия"',
            'meta_description': 'Тест-мета-описание "Условия"'
        }
        response = self.user_client.get(url)
        response_data = response.data[0]
        for key, value in expected_data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(
                    response_data[key], value
                )

    def test_contacts_viewset(self):
        """Проверка эндпоинта contacts."""
        url = '/api/core/contacts/'
        image_url = 'http://testserver'
        expected_data = {
            'headline': 'Тест-заглавие "Контакты"',
            'meta_title': 'Тест-мета-заглавие "Контакты"',
            'meta_description': 'Тест-мета-описание "Контакты"',
            'requisites': [
                {
                    'requisite_name': 'Тестовый реквизит',
                    'requisite_description': 'Тестовое описание'
                },
                {
                    'requisite_name': 'Тестовый реквизит 2',
                    'requisite_description': 'Тестовое описание 2'
                }
            ],
            'main_shop': {
                'name': 'Тестовый магазин на дворе',
                'comment': 'Будни с 8:00 до 20:00',
                'phone_number': '1234567890',
                'email': 'test@test.test',
                'location': 'Тестовая локация'
            },
            'our_shops': [
                {
                    'name': 'Тестовый магазин за углом',
                    'comment': 'Будни с 20:00 до 8:00',
                    'phone_number': '0987654321',
                    'photo': (
                        image_url +
                        InfoModelsViewsTest.our_shop.photo.url
                    ),
                    'is_main_shop': True
                },
                {
                    'name': 'Тестовый магазин на дворе',
                    'comment': 'Будни с 8:00 до 20:00',
                    'phone_number': '1234567890',
                    'photo': (
                        image_url +
                        InfoModelsViewsTest.our_shop_2.photo.url
                    ),
                    'is_main_shop': False
                }
            ],
            'mail_form': {
                'headline': 'Тестовый заголовок формы',
                'ask_name': 'Введите имя',
                'ask_email': 'Введите e-mail',
                'ask_message': 'Введите сообщение',
                'send_button_text': 'Отправить',
            }
        }
        response = self.user_client.get(url)
        response_data = response.data[0]
        for key, value in expected_data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(
                    response_data[key], value
                )

    def tearDown(self):
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


class MailContactTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mail_1 = MailContact.objects.create(
            person_name='Тест Тестович',
            person_email='test@test.test',
            message='Тестовое обращение'
        )

    def setUp(self):
        super().setUp()
        self.mail_url = '/api/core/contacts/mail/'
        self.client = APIClient()

    def test_mail_contact_post(self):
        """Проверка отправки POST-запроса."""
        start_object_count = MailContact.objects.count()
        post_data = {
            'person_name': 'Тест Тестович',
            'person_email': 'test@test.test',
            'message': 'Тестовое обращение 2'
        }
        response = self.client.post(
            self.mail_url,
            data=post_data
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        objects_count = start_object_count + 1
        self.assertEqual(MailContact.objects.count(), objects_count)

    def tearDown(self):
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class BaseElementsTestCase(TestCase):

    image_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    image = SimpleUploadedFile(
        'image_gif.gif',
        image_gif,
        content_type='image/gif'
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.header = Header.objects.create()
        cls.footer = Footer.objects.create(
            company_info='Тестовая компания',
            disclaimer='Ваши тесты защищены',
            support_work_time='Работаем в тестовом режиме'
        )
        cls.main_logo = MainLogo.objects.create(
            image=cls.image,
            url='https://test.com',
            header=cls.header,
            footer=cls.footer
        )
        cls.add_logo_1 = AdditionalLogo.objects.create(
            image=cls.image,
            url='https://test2.com',
            footer=cls.footer
        )
        cls.add_logo_2 = AdditionalLogo.objects.create(
            image=cls.image,
            url='https://test3.com',
            footer=cls.footer
        )
        cls.support = Support.objects.create(
            name='Тестовая поддержка',
            phone_number='1234567890',
            header=cls.header,
            footer=cls.footer
        )

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_base_elements_viewset(self):
        """Проверка эндпоинта base."""
        url = '/api/core/base/'
        image_url = 'https://testserver'
        expected_data = {
            'header': {
                'support': {
                    'name': 'Тестовая поддержка',
                    'phone_number': '1234567890',
                },
                'main_logo': {
                    'image':
                        image_url + BaseElementsTestCase.main_logo.image.url,
                    'url': 'https://test.com'
                },
            },
            'footer': {
                'company_info': 'Тестовая компания',
                'disclaimer': 'Ваши тесты защищены',
                'support_work_time': 'Работаем в тестовом режиме',
                'main_logo': {
                    'image': (
                        image_url +
                        BaseElementsTestCase.main_logo.image.url
                    ),
                    'url': 'https://test.com'
                },
                'additional_logos': [
                    {
                        'image': (
                            image_url +
                            BaseElementsTestCase.add_logo_1.image.url
                        ),
                        'url': 'https://test2.com'
                    },
                    {
                        'image': (
                            image_url +
                            BaseElementsTestCase.add_logo_2.image.url
                        ),
                        'url': 'https://test3.com'
                    }
                ],
                'support': {
                    'name': 'Тестовая поддержка',
                    'phone_number': '1234567890',
                }
            }
        }
        response = self.client.get(url, secure=True)
        response_data = response.data
        for key, value in expected_data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(
                    response_data[key], value
                )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
