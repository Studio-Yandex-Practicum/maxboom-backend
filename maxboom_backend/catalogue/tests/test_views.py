import shutil
import tempfile

from catalogue.models import Brand, Category, Product, ProductImage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CatalogueViewsTests(TestCase):
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
            name='Бренд',
            is_prohibited=False,
            is_visible_on_main=True,
            image=cls.uploaded
        )
        cls.brand_prohibited = Brand.objects.create(
            name='Производитель',
            is_prohibited=True,
            is_visible_on_main=True,
            image=cls.uploaded
        )
        cls.category_root = Category.objects.create(
            name='Категория тестовая корневая',
        )
        cls.category_root_prohibited = Category.objects.create(
            name='Категория тестовая корневая 1',
            is_prohibited=True,
        )
        cls.category_branch = Category.objects.create(
            name='Категория промежуточная',
            root=cls.category_root,
        )
        cls.category = Category.objects.create(
            name='Категория1',
            meta_title='мета-название',
            meta_description='мета-описание',
            is_visible_on_main=True,
            is_prohibited=False,
            root=cls.category_branch,
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
            meta_title='test_title',
            meta_description='test description',
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
        cls.product_deleted = Product.objects.create(
            name='Пусковое зарядное устройство 3',
            description='Хороший продукт для',
            price=180,
            brand=cls.brand,
            category=cls.category,
            code=169110395,
            wb_urls='https://www.wildberries.ru/catalog/169110395/detail.aspx',
            is_deleted=True,
            meta_title='test_title',
            meta_description='test description',
        )
        cls.uploaded = SimpleUploadedFile(
            name='prod_add_img.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.image = ProductImage.objects.create(
            product=cls.product_deleted,
            image=cls.uploaded
        )
        cls.user = User.objects.create_user(
            'user_new@example.com', 'test_pass')

    def setUp(self):
        self.user_client = APIClient()
        self.user_authorized_client = APIClient()
        self.user_authorized_client.force_authenticate(
            CatalogueViewsTests.user)

    def test_user_get_list_root_categories(self):
        '''получение категорий'''
        address = '/api/catalogue/categories/'
        response = self.user_client.get(address)
        categories_count = len(response.data)
        self.assertEqual(1, categories_count,
                         'Пользователь получил категории'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'id': 1,
                'name': 'Категория тестовая корневая',
                'slug': 'kategoriya-testovaya-kornevaya',
                'meta_title': None,
                'meta_description': None,
                'products': [],
                'branches': [
                    {
                        'id': 3,
                        'name': 'Категория промежуточная',
                        'slug': 'kategoriya-promezhutochnaya',
                        'branches': [
                            {
                                'id': 4,
                                'name': 'Категория1',
                                'slug': 'kategoriya1',
                                'branches': []
                            }
                        ]
                    }
                ],
                'root': None
            }
        ]
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_item_category(self):
        '''получение отдельной категории'''
        category = CatalogueViewsTests.category
        price = round(CatalogueViewsTests.product.price * 0.8, 2)
        address = f'/api/catalogue/categories/{category.slug}/'
        response = self.user_client.get(address)
        expected_data = {
            'id': 4,
            'name': 'Категория1',
            'slug': 'kategoriya1',
            'meta_title': 'мета-название',
            'meta_description': 'мета-описание',
            'products': [
                {
                    'id': 1,
                    'category': 'Категория1',
                    'brand': 'Бренд',
                    'images': [
                        {
                            'image': ('http://testserver/media/'
                                      'products-images/prod_img.gif')
                        }
                    ],
                    'price': price,
                    'name': 'Пусковое зарядное устройство 2',
                    'slug': 'puskovoe-zaryadnoe-ustrojstvo-2',
                    'description': 'Хороший продукт для',
                    'code': 169110394,
                    'wb_urls': ('https://www.wildberries.ru/catalog/'
                                '169110394/detail.aspx'),
                    'quantity': 999999.0,
                    'is_deleted': False,
                    'meta_title': 'test_title',
                    'meta_description': 'test description'
                }
            ],
            'branches': [],
            'root': {
                'id': 3,
                'name': 'Категория промежуточная',
                'slug': 'kategoriya-promezhutochnaya',
                'root': {
                    'id': 1,
                    'name': 'Категория тестовая корневая',
                    'slug': 'kategoriya-testovaya-kornevaya',
                    'root': None
                }
            }
        }
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_list_brands(self):
        '''получение списка производителей'''
        address = '/api/catalogue/brands/'
        price = round(CatalogueViewsTests.product.price * 0.8, 2)
        response = self.user_client.get(address)
        brands_count = len(response.data)
        self.assertEqual(1, brands_count,
                         'Пользователь получил бренды'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'id': 1,
                'name': 'Бренд',
                'slug': 'brend',
                'products': [
                    {
                        'id': 1,
                        'category': 'Категория1',
                        'brand': 'Бренд',
                        'images': [
                            {
                                'image': ('http://testserver/media/'
                                          'products-images/prod_img.gif')
                            }
                        ],
                        'price': price,
                        'name': 'Пусковое зарядное устройство 2',
                        'slug': 'puskovoe-zaryadnoe-ustrojstvo-2',
                        'description': 'Хороший продукт для',
                        'code': 169110394,
                        'wb_urls': ('https://www.wildberries.ru/catalog/'
                                    '169110394/detail.aspx'),
                        'quantity': 999999.0,
                        'is_deleted': False,
                        'meta_title': 'test_title',
                        'meta_description': 'test description'
                    }
                ],
                'image': 'http://testserver/media/brand-images/logo_brand.gif',
                'is_prohibited': False,
                'is_visible_on_main': True
            }
        ]
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_item_brand(self):
        '''получение отдельного производителя'''
        brand = CatalogueViewsTests.brand
        price = round(CatalogueViewsTests.product.price * 0.8, 2)
        address = f'/api/catalogue/brands/{brand.slug}/'
        response = self.user_client.get(address)
        expected_data = {
            'id': 1,
            'name': 'Бренд',
            'slug': 'brend',
            'products': [
                {
                    'id': 1,
                    'category': 'Категория1',
                    'brand': 'Бренд',
                    'images': [
                        {
                            'image': ('http://testserver/media/'
                                      'products-images/prod_img.gif')
                        }
                    ],
                    'price': price,
                    'name': 'Пусковое зарядное устройство 2',
                    'slug': 'puskovoe-zaryadnoe-ustrojstvo-2',
                    'description': 'Хороший продукт для',
                    'code': 169110394,
                    'wb_urls': ('https://www.wildberries.ru/catalog/'
                                '169110394/detail.aspx'),
                    'quantity': 999999.0,
                    'is_deleted': False,
                    'meta_title': 'test_title',
                    'meta_description': 'test description'
                }
            ],
            'image': 'http://testserver/media/brand-images/logo_brand.gif',
            'is_prohibited': False,
            'is_visible_on_main': True
        }
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_list_products(self):
        '''получение списка товаров'''
        address = '/api/catalogue/products/'
        price = round(CatalogueViewsTests.product.price * 0.8, 2)
        response = self.user_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(1, products_count,
                         'Пользователь получил товары'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'id': 1,
                'category': {
                    'id': 4,
                    'name': 'Категория1',
                    'slug': 'kategoriya1',
                    'root': {
                        'id': 3,
                        'name': 'Категория промежуточная',
                        'slug': 'kategoriya-promezhutochnaya',
                        'root': {
                            'id': 1,
                            'name': 'Категория тестовая корневая',
                            'slug': 'kategoriya-testovaya-kornevaya',
                            'root': None
                        }
                    }
                },
                'brand': 'Бренд',
                'images': [
                    {
                        'image': ('http://testserver/media/'
                                  'products-images/prod_img.gif')
                    }
                ],
                'price': price,
                'name': 'Пусковое зарядное устройство 2',
                'slug': 'puskovoe-zaryadnoe-ustrojstvo-2',
                'description': 'Хороший продукт для',
                'code': 169110394,
                'wb_urls': ('https://www.wildberries.ru/catalog/'
                            '169110394/detail.aspx'),
                'quantity': 999999.0,
                'is_deleted': False,
                'meta_title': 'test_title',
                'meta_description': 'test description'
            }
        ]
        self.check_fields(response=response.data.get(
            'results'), expected_data=expected_data)

    def test_user_get_item_product(self):
        '''получение товара цена со скидкой 20%'''
        product = CatalogueViewsTests.product
        price = round(product.price * 0.8, 2)
        address = f'/api/catalogue/products/{product.slug}/'
        response = self.user_client.get(address)
        expected_data = {
            'id': 1,
            'category': {
                'id': 4,
                'name': 'Категория1',
                'slug': 'kategoriya1',
                'root': {
                    'id': 3,
                    'name': 'Категория промежуточная',
                    'slug': 'kategoriya-promezhutochnaya',
                    'root': {
                        'id': 1,
                        'name': 'Категория тестовая корневая',
                        'slug': 'kategoriya-testovaya-kornevaya',
                        'root': None
                    }
                }
            },
            'brand': 'Бренд',
            'images': [
                {
                    'image': ('http://testserver/media/'
                              'products-images/prod_img.gif')
                }
            ],
            'price': price,
            'name': 'Пусковое зарядное устройство 2',
            'slug': 'puskovoe-zaryadnoe-ustrojstvo-2',
            'description': 'Хороший продукт для',
            'code': 169110394,
            'wb_urls': ('https://www.wildberries.ru/catalog/'
                        '169110394/detail.aspx'),
            'quantity': 999999.0,
            'is_deleted': False,
            'meta_title': 'test_title',
            'meta_description': 'test description'
        }
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_authorized_get_item_product(self):
        '''получение товара цена со скидкой 50%'''
        product = CatalogueViewsTests.product
        price = round(product.price * 0.5, 2)
        address = f'/api/catalogue/products/{product.slug}/'
        response = self.user_authorized_client.get(address)
        expected_data = {
            'id': 1,
            'category': {
                'id': 4,
                'name': 'Категория1',
                'slug': 'kategoriya1',
                'root': {
                    'id': 3,
                    'name': 'Категория промежуточная',
                    'slug': 'kategoriya-promezhutochnaya',
                    'root': {
                        'id': 1,
                        'name': 'Категория тестовая корневая',
                        'slug': 'kategoriya-testovaya-kornevaya',
                        'root': None
                    }
                }
            },
            'brand': 'Бренд',
            'images': [
                {
                    'image': ('http://testserver/media/'
                              'products-images/prod_img.gif')
                }
            ],
            'price': price,
            'name': 'Пусковое зарядное устройство 2',
            'slug': 'puskovoe-zaryadnoe-ustrojstvo-2',
            'description': 'Хороший продукт для',
            'code': 169110394,
            'wb_urls': ('https://www.wildberries.ru/catalog/'
                        '169110394/detail.aspx'),
            'quantity': 999999.0,
            'is_deleted': False,
            'meta_title': 'test_title',
            'meta_description': 'test description'
        }
        self.check_fields(response=response.data, expected_data=expected_data)

    def check_fields(self, response, expected_data):
        if type(expected_data) is list and expected_data:
            for i in range(len(expected_data)):
                self.check_fields(
                    response=response[i], expected_data=expected_data[i])
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

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
