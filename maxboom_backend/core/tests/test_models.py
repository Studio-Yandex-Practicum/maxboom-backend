# flake8: noqa
import tempfile
import shutil

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import (
    About, DeliveryInformation, Privacy, Terms,
    Contacts, Requisite, MainShop, OurShop,
    MailContactForm, MailContact, Header, Footer,
    MainLogo, AdditionalLogo, Support
)


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class InfoModelTest(TestCase):

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

    def test_models_have_correct_names(self):
        """Проверка вывода названий объектов методом str()."""
        objects = {
            About: InfoModelTest.about,
            DeliveryInformation: InfoModelTest.delivery,
            Privacy: InfoModelTest.privacy,
            Terms: InfoModelTest.terms,
            Contacts: InfoModelTest.contacts
        }
        for model, obj in objects.items():
            with self.subTest(model=model):
                self.assertEqual(
                    model._meta.verbose_name, str(obj)
                )

    def models_have_correct_representation_name(self):
        """Проверка вывода названий объектов методом repr()."""
        objects = {
            About: InfoModelTest.about,
            DeliveryInformation: InfoModelTest.delivery,
            Privacy: InfoModelTest.privacy,
            Terms: InfoModelTest.terms,
            Contacts: InfoModelTest.contacts
        }
        for model, obj in objects.items():
            with self.subTest(model=model):
                self.assertEqual(
                    model.__name__, repr(obj)
                )

    def test_model_fields_have_correct_texts(self):
        """Проверка соответствия описаний полей."""
        text_data = {
            'headline': {
                'verbose_name': 'Заголовок страницы',
                'help_text': 'Введите заголовок страницы'
            },
            'text': {
                'verbose_name': 'Текст страницы',
                'help_text': 'Введите текст страницы'
            },
            'meta_title': {
                'verbose_name': 'Мета-название страницы',
            },
            'meta_description': {
                'verbose_name': 'Мета-описание страницы'
            }
        }
        objects = [
            InfoModelTest.about,
            InfoModelTest.delivery,
            InfoModelTest.privacy,
            InfoModelTest.terms,
            InfoModelTest.contacts
        ]
        for obj in objects:
            if obj.__class__ == Contacts:
                text_data.pop('text')
            for field, data in text_data.items():
                with self.subTest(field=field, data=data):
                    self.assertEqual(
                        obj._meta.get_field(field).verbose_name,
                        data['verbose_name']
                    )
                    if data.get('help_text'):
                        self.assertEqual(
                            obj._meta.get_field(field).help_text,
                            data['help_text']
                        )

    def test_models_ordering(self):
        """Проверка порядка вывода моделей."""
        new_data = {
            'headline': 'Тест-заглавие 2"',
            'text': 'Тест-текст 2',
            'meta_title': 'Тест-мета-заглавие 2',
            'meta_description': 'Тест-мета-описание 2'
        }
        models = [About, DeliveryInformation, Privacy, Terms, Contacts]
        for model in models:
            if model == Contacts:
                new_data.pop('text')
            model.objects.create(**new_data)
        objects = [
            InfoModelTest.about,
            InfoModelTest.delivery,
            InfoModelTest.privacy,
            InfoModelTest.terms,
            InfoModelTest.contacts
        ]
        objects_dict = dict(zip(models, objects))
        for model, obj in objects_dict.items():
            model_objs = model.objects.all()
            with self.subTest(models=model, object=obj):
                self.assertEqual(obj, model_objs[0])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class ContactsPageTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.contacts = Contacts.objects.create(
            headline='Тест-заглавие "Контакты"',
            meta_title='Тест-мета-заглавие "Контакты"',
            meta_description='Тест-мета-описание "Контакты"'
        )

    def test_contacts_have_correct_name(self):
        """Проверка правильного отображения контактов методом str()."""
        contacts = ContactsPageTestCase.contacts
        self.assertEqual(contacts._meta.verbose_name, str(contacts))

    def test_contacts_have_correct_representation_name(self):
        """Проверка правильного отображения контактов методом repr()."""
        contacts = ContactsPageTestCase.contacts
        self.assertEqual(Contacts.__name__, repr(contacts))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class RequisiteTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.requisite_1 = Requisite.objects.create(
            requisite_name='Тестовый реквизит 1',
            requisite_description='Описание реквизита 1'
        )

    def test_requisite_have_correct_name(self):
        """Проверка правильного отображения реквизитов методом str()."""
        requisite = RequisiteTestCase.requisite_1
        self.assertEqual(requisite._meta.verbose_name, str(requisite))

    def test_requisite_have_correct_representation_name(self):
        """Проверка правильного отображения реквизитов методом repr()."""
        requisite = RequisiteTestCase.requisite_1
        self.assertEqual(Requisite.__name__, repr(requisite))

    def test_requisite_have_correct_field_text(self):
        """Проверка соответствия описаний полей."""
        text_data = {
            'requisite_name': {
                'verbose_name': 'Название реквизита',
                'help_text': 'Укажите название реквизита'
            },
            'requisite_description': {
                'verbose_name': 'Описание реквизита',
                'help_text': 'Укажите описание реквизита'
            }
        }
        requisite = RequisiteTestCase.requisite_1
        for field, data in text_data.items():
            with self.subTest(field=field, data=data):
                self.assertEqual(
                    requisite._meta.get_field(field).verbose_name,
                    data['verbose_name']
                )
                self.assertEqual(
                    requisite._meta.get_field(field).help_text,
                    data['help_text']
                )

    def test_requisite_have_null_contacts(self):
        """Проверка наличия у реквизитов пустого поля страницы."""
        contacts = RequisiteTestCase.requisite_1.main_page
        self.assertEqual(contacts, None)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class MailContactFormTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = MailContactForm.objects.create(
            headline='Тестовая форма',
            ask_name='Ваше имя',
            ask_email='Ваш E-mail',
            ask_message='Ваше сообщение',
            send_button_text='Отправить'
        )

    def test_mail_form_have_correct_name(self):
        """Проверка правильного отображения формы методом str()."""
        form = MailContactFormTestCase.form
        self.assertEqual(form._meta.verbose_name, str(form))

    def test_mail_form_have_correct_representation_name(self):
        """Проверка правильного отображения формы методом repr()."""
        form = MailContactFormTestCase.form
        self.assertEqual(MailContactForm.__name__, repr(form))

    def test_mail_form_fields_have_correct_text(self):
        """Проверка правильного отображения текстов полей."""
        text_data = {
            'headline': {
                'verbose_name': 'Заголовок формы'
            },
            'ask_name': {
                'verbose_name': 'Поле для имени'
            },
            'ask_email': {
                'verbose_name': 'Поле для E-Mail'
            },
            'ask_message': {
                'verbose_name': 'Поле для сообщения'
            },
            'send_button_text': {
                'verbose_name': 'Текст на кнопке отправки'
            }
        }
        form = MailContactFormTestCase.form
        for field, data in text_data.items():
            with self.subTest(field=field, data=data):
                self.assertEqual(
                    form._meta.get_field(field).verbose_name,
                    data['verbose_name']
                )

    def test_mail_form_correct_ordering(self):
        """Проверка правильного упорядочивания."""
        MailContactForm.objects.create(
            headline='Тестовая форма 2',
            ask_name='Ваше имя 2',
            ask_email='Ваш E-mail 2',
            ask_message='Ваше сообщение 2',
            send_button_text='Отправить 2'
        )
        forms = MailContactForm.objects.all()
        self.assertEqual(self.form, forms[0])

    def test_mail_form_have_null_contacts(self):
        """Проверка наличия у формы пустого поля страницы."""
        form = MailContactFormTestCase.form.main_page
        self.assertEqual(form, None)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class MainShopTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shop = MainShop.objects.create(
            name='Тестовый магазин на дворе',
            comment='Будни с 8:00 до 20:00',
            phone_number='1234567890',
            email='test@test.test',
            location='Тестовая локация'
        )

    def test_shop_have_correct_name(self):
        """Проверка правильного отображения объекта методом str()."""
        shop = MainShopTestCase.shop
        self.assertEqual(shop._meta.verbose_name, str(shop))

    def test_shop_have_correct_representation_name(self):
        """Проверка правильного отображения объекта методом repr()."""
        shop = MainShopTestCase.shop
        self.assertEqual(MainShop.__name__, repr(shop))

    def test_shop_fields_have_correct_text(self):
        """Проверка правильности текстов полей."""
        text_data = {
            'name': {
                'verbose_name': 'Название магазина',
                'help_text': 'Укажите название магазина'
            },
            'comment': {
                'verbose_name': 'Комментарий о магазине',
                'help_text': 'Время работы и дополнительная информация'
            },
            'phone_number': {
                'verbose_name': 'Номер телефона',
                'help_text': 'Укажите номер телефона магазина'
            },
            'email': {
                'verbose_name': 'Почта магазина',
                'help_text': 'Введите электронную почту магазина'
            },
            'location': {
                'verbose_name': 'Адрес магазина',
                'help_text': 'Укажите адрес магазина'
            }
        }
        shop = MainShopTestCase.shop
        for field, data in text_data.items():
            with self.subTest(field=field, data=data):
                self.assertEqual(
                    shop._meta.get_field(field).verbose_name,
                    data['verbose_name']
                )
                self.assertEqual(
                    shop._meta.get_field(field).help_text,
                    data['help_text']
                )

    def test_shop_ordering(self):
        """Проверка правильности упорядочивания модели."""
        MainShop.objects.create(
            name='Тестовый магазин за углом',
            comment='Будни с 20:00 до 8:00',
            phone_number='0987654321',
            email='test2@test2.test',
            location='Тестовая локация 2'
        )
        shops = MainShop.objects.all()
        self.assertEqual(shops[0], self.shop)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OurShopTestCase(TestCase):

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
        cls.shop = OurShop.objects.create(
            name='Тестовый магазин на дворе',
            comment='Будни с 8:00 до 20:00',
            phone_number='1234567890',
            photo=cls.image,
            is_main_shop=True
        )

    def test_shop_have_correct_name(self):
        """Проверка правильного отображения объекта методом str()."""
        shop = OurShopTestCase.shop
        self.assertEqual(shop._meta.verbose_name, str(shop))

    def test_shop_have_correct_representation_name(self):
        """Проверка правильного отображения объекта методом repr()."""
        shop = OurShopTestCase.shop
        self.assertEqual(OurShop.__name__, repr(shop))

    def test_shop_fields_have_correct_text(self):
        """Проверка правильности текстов полей."""
        text_data = {
            'name': {
                'verbose_name': 'Название магазина',
                'help_text': 'Укажите название магазина'
            },
            'comment': {
                'verbose_name': 'Комментарий о магазине',
                'help_text': 'Время работы и дополнительная информация'
            },
            'phone_number': {
                'verbose_name': 'Номер телефона',
                'help_text': 'Укажите номер телефона магазина'
            },
            'photo': {
                'verbose_name': 'Фотография',
            },
            'is_main_shop': {
                'verbose_name': 'Основной магазин',
                'help_text': 'Укажите статус магазина как основного'
            }
        }
        shop = OurShopTestCase.shop
        for field, data in text_data.items():
            with self.subTest(field=field, data=data):
                self.assertEqual(
                    shop._meta.get_field(field).verbose_name,
                    data['verbose_name']
                )
                if data.get('help_text'):
                    self.assertEqual(
                        shop._meta.get_field(field).help_text,
                        data['help_text']
                    )

    def test_objects_creating_correctly(self):
        """Проверка создания новых объектов."""
        OurShop.objects.create(
            name='Тестовый магазин за углом',
            comment='Будни с 20:00 до 8:00',
            phone_number='0987654321',
            photo=OurShopTestCase.image,
            is_main_shop=True
        )
        total_objects = OurShop.objects.count()
        self.assertEqual(total_objects, 2)

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
            message='Тестовое сообщение'
        )

    def test_mail_contact_have_correct_name(self):
        """Проверка правильного вывода методом str()."""
        mail_contact = MailContactTestCase.mail_1
        self.assertEqual(MailContact._meta.verbose_name, str(mail_contact))

    def test_mail_contact_have_correct_representation(self):
        """Проверка правильного вывода методом str()."""
        mail_contact = MailContactTestCase.mail_1
        self.assertEqual(MailContact.__name__, repr(mail_contact))

    def test_mail_contact_have_correct_texts(self):
        """Проверка правильных текстов полей."""
        text_data = {
            'person_name': {
                'verbose_name': 'Имя',
                'help_text': 'Имя'

            },
            'person_email': {
                'verbose_name': 'E-mail',
                'help_text': 'E-Mail'

            },
            'message': {
                'verbose_name': 'Текст сообщения или вопроса',
                'help_text': 'Текст сообщения или вопроса'
            }
        }
        mail_contact = MailContactTestCase.mail_1
        for field, data in text_data.items():
            with self.subTest(field=field, data=data):
                self.assertEqual(
                    mail_contact._meta.get_field(field).verbose_name,
                    data['verbose_name']
                )
                self.assertEqual(
                    mail_contact._meta.get_field(field).help_text,
                    data['help_text']
                )

    def test_objects_creating_correctly(self):
        """Проверка создания новых объектов."""
        MailContact.objects.create(
            person_name='Тест Тестович 2',
            person_email='test2@test.test',
            message='Тестовое сообщение 2'
        )
        total_objects = MailContact.objects.count()
        self.assertEqual(total_objects, 2)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class HeaderTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.header = Header.objects.create()

    def test_footer_have_correct_name(self):
        """Проверка правильного вывода методом str()."""
        header = HeaderTestCase.header
        self.assertEqual(Header._meta.verbose_name, str(header))

    def test_header_have_correct_representation(self):
        """Проверка правильного вывода методом str()."""
        header = HeaderTestCase.header
        self.assertEqual(Header.__name__, repr(header))

    def test_header_ordering(self):
        """Проверка упорядочивания объектов."""
        header = HeaderTestCase.header
        Header.objects.create()
        header_objects = Header.objects.all()
        self.assertEqual(header, header_objects[0])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class FooterTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.footer = Footer.objects.create(
            company_info='Тестовая компания',
            disclaimer='Тестовый дисклеймер',
            support_work_time='Будни 8:00-20?00'
        )

    def test_header_have_correct_name(self):
        """Проверка правильного вывода методом str()."""
        footer = FooterTestCase.footer
        self.assertEqual(Footer._meta.verbose_name, str(footer))

    def test_header_have_correct_representation(self):
        """Проверка правильного вывода методом str()."""
        footer = FooterTestCase.footer
        self.assertEqual(Footer.__name__, repr(footer))

    def test_fields_have_correct_verbose_name(self):
        """Проверка правильных текстов у полей футера."""
        text_data = {
            'company_info': {
                'verbose_name': 'Информация о компании внизу страницы'
            },
            'disclaimer': {
                'verbose_name': 'Авторство внизу страницы'
            },
            'support_work_time': {
                'verbose_name': 'Время работы поддержки'
            }
        }
        footer = FooterTestCase.footer
        for field, data in text_data.items():
            with self.subTest(field=field, data=data):
                self.assertEqual(
                    footer._meta.get_field(field).verbose_name,
                    data['verbose_name']
                )

    def test_header_ordering(self):
        """Проверка упорядочивания объектов."""
        footer = FooterTestCase.footer
        Footer.objects.create()
        footer_objects = Footer.objects.all()
        self.assertEqual(footer, footer_objects[0])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class MainLogoTestCase(TestCase):

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
        cls.logo = MainLogo.objects.create(
            image=cls.image,
            url='https://test.test'
        )

    def test_logo_have_correct_name(self):
        """Проверка правильного вывода методом str()."""
        logo = MainLogoTestCase.logo
        self.assertEqual(MainLogo._meta.verbose_name, str(logo))

    def test_logo_have_correct_representation(self):
        """Проверка правильного вывода методом str()."""
        logo = MainLogoTestCase.logo
        self.assertEqual(MainLogo.__name__, repr(logo))

    def test_fields_have_correct_verbose_name(self):
        """Проверка правильных текстов у полей логотипа."""
        text_data = {
            'image': {
                'verbose_name': 'Изображение логотипа'
            },
            'url': {
                'verbose_name': 'Ссылка на сайт логотипа'
            }
        }
        logo = MainLogoTestCase.logo
        for field, data in text_data.items():
            with self.subTest(field=field, data=data):
                self.assertEqual(
                    logo._meta.get_field(field).verbose_name,
                    data['verbose_name']
                )

    def test_header_ordering(self):
        """Проверка упорядочивания объектов."""
        logo = MainLogoTestCase.logo
        MainLogo.objects.create(
            image=MainLogoTestCase.image,
            url='https://test2.test'
        )
        logo_objects = MainLogo.objects.all()
        self.assertEqual(logo, logo_objects[0])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class AdditionalLogoTestCase(TestCase):

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
        cls.logo = AdditionalLogo.objects.create(
            image=cls.image,
            url='https://test.test'
        )

    def test_logo_have_correct_name(self):
        """Проверка правильного вывода методом str()."""
        logo = AdditionalLogoTestCase.logo
        self.assertEqual(AdditionalLogo._meta.verbose_name, str(logo))

    def test_logo_have_correct_representation(self):
        """Проверка правильного вывода методом str()."""
        logo = AdditionalLogoTestCase.logo
        self.assertEqual(AdditionalLogo.__name__, repr(logo))

    def test_fields_have_correct_verbose_name(self):
        """Проверка правильных текстов у полей логотипа."""
        text_data = {
            'image': {
                'verbose_name': 'Изображение логотипа'
            },
            'url': {
                'verbose_name': 'Ссылка на сайт логотипа'
            }
        }
        logo = AdditionalLogoTestCase.logo
        for field, data in text_data.items():
            with self.subTest(field=field, data=data):
                self.assertEqual(
                    logo._meta.get_field(field).verbose_name,
                    data['verbose_name']
                )

    def test_new_objects_creating(self):
        """Проверка создания нового объекта."""
        AdditionalLogo.objects.create(
            image=AdditionalLogoTestCase.image,
            url='https://test2.test'
        )
        objects_count = AdditionalLogo.objects.count()
        self.assertEqual(objects_count, 2)

    def test_header_ordering(self):
        """Проверка упорядочивания объектов."""
        logo = AdditionalLogoTestCase.logo
        AdditionalLogo.objects.create(
            image=AdditionalLogoTestCase.image,
            url='https://test2.test'
        )
        logo_objects = AdditionalLogo.objects.all()
        self.assertEqual(logo, logo_objects[0])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


class SupportTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.support = Support.objects.create(
            name='Тестовая поддержка',
            phone_number='1234567890'
        )

    def test_support_have_correct_name(self):
        """Проверка правильного вывода методом str()."""
        support = SupportTestCase.support
        self.assertEqual(Support._meta.verbose_name, str(support))

    def test_support_have_correct_representation(self):
        """Проверка правильного вывода методом str()."""
        support = SupportTestCase.support
        self.assertEqual(Support.__name__, repr(support))

    def test_header_ordering(self):
        """Проверка упорядочивания объектов."""
        Support.objects.create(
            name='Тестовая поддержка 2',
            phone_number='0987654321'
        )
        support = SupportTestCase.support
        support_objects = Support.objects.all()
        self.assertEqual(support, support_objects[0])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
