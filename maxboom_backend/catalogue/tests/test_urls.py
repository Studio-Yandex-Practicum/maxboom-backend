import shutil
import tempfile
from http import HTTPStatus

from catalogue.models import Brand, Category, Product, ProductImage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CatalogueURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='logo_brand.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.brand = Brand.objects.create(
            name='Производитель',
            is_prohibited=False,
            is_visible_on_main=True,
            image=cls.uploaded
        )
        cls.category_root = Category.objects.create(
            name='Категория тестовая',
        )
        cls.category = Category.objects.create(
            name='Подкатегория',
            is_visible_on_main=True,
            is_prohibited=False,
            root=cls.category_root,
        )
        cls.product = Product.objects.create(
            name='Пусковое зарядное устройство 2',
            description='Хороший продукт для',
            price=180,
            brand=cls.brand,
            category=cls.category,
            code=169110394,
            wb_urls='https://www.wildberries.ru/catalog/169110394/detail.aspx',
            is_deleted=False,
        )
        cls.uploaded = SimpleUploadedFile(
            name='prod_img.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.image = ProductImage.objects.create(
            product=cls.product,
            image=cls.uploaded
        )

    def setUp(self):
        self.user_client = APIClient()

    def test_user_get_urls(self):
        '''доступные пользователям url'''
        brand = CatalogueURLTests.brand
        category = CatalogueURLTests.category
        category_root = CatalogueURLTests.category_root
        product = CatalogueURLTests.product
        status_pages = {
            '/api/catalogue/brand/': HTTPStatus.OK,
            f'/api/catalogue/brand/{brand.slug}/': HTTPStatus.OK,
            '/api/catalogue/category/': HTTPStatus.OK,
            f'/api/catalogue/category/{category_root.slug}/': HTTPStatus.OK,
            f'/api/catalogue/category/{category.slug}/': HTTPStatus.OK,
            '/api/catalogue/': HTTPStatus.OK,
            f'/api/catalogue/{product.slug}/': HTTPStatus.OK,
            # f'{brand.image.url}': HTTPStatus.OK,

        }
        for address, code in status_pages.items():
            with self.subTest(address=address):
                response = self.user_client.get(address)
                self.assertEqual(response.status_code, code, f'{address}')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
