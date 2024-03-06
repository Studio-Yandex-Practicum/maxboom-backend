import shutil
import tempfile
# from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from catalogue.models import Brand, Category, Product, ProductImage

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
            is_visible_on_main=False,
            image=cls.uploaded
        )
        cls.brand_prohibited = Brand.objects.create(
            name='Производитель',
            is_prohibited=True,
            is_visible_on_main=True,
            image=cls.uploaded
        )
        cls.brand_is_visible_on_main = Brand.objects.create(
            name='хMaxBoom',
            is_prohibited=False,
            is_visible_on_main=True,
            image=cls.uploaded
        )
        cls.category_root = Category.objects.create(
            name='Корневая категория',
            wb_category_id=123452
        )
        cls.category_root_prohibited = Category.objects.create(
            name='Корневая категория 1',
            is_prohibited=True,
            wb_category_id=123453
        )
        cls.category_branch = Category.objects.create(
            name='Подкатегория',
            root=cls.category_root,
            wb_category_id=123454
        )
        cls.category = Category.objects.create(
            name='Категория1',
            is_visible_on_main=True,
            is_prohibited=False,
            root=cls.category_branch,
            wb_category_id=123455
        )
        cls.product = Product.objects.create(
            name='Пусковое зарядное устройство 2 для поиска',
            description='Хороший продукт для description search',
            price=180,
            brand=cls.brand,
            category=cls.category,
            code=169110394,
            vendor_code='артикул 6',
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
        cls.product_deleted = Product.objects.create(
            name='Пусковое зарядное устройство 3',
            description='Хороший продукт для',
            price=180,
            brand=cls.brand,
            category=cls.category,
            code=169110395,
            vendor_code='артикул 7',
            wb_urls=(
                'https://www.wildberries.ru/catalog/169110395/detail.aspx'
            ),
            is_deleted=True,
        )
        cls.product_in_root_cat = Product.objects.create(
            name='Пусковое зарядное устройство 4',
            description='Хороший продукт для 4',
            price=180,
            brand=cls.brand,
            category=cls.category_root,
            code=1691103959,
            vendor_code='артикул 8',
            wb_urls=(
                'https://www.wildberries.ru/catalog/1691103959/detail.aspx'
            ),
            is_deleted=False,
        )
        cls.product_in_branches = Product.objects.create(
            name='Пусковое зарядное устройство 5',
            description='Хороший продукт для',
            price=180,
            brand=cls.brand,
            category=cls.category_branch,
            code=1691103945,
            vendor_code='артикул 9',
            wb_urls=(
                'https://www.wildberries.ru/catalog/1691103945/detail.aspx'
            ),
            is_deleted=False,
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
        cls.user.userprofile.is_vendor = True
        cls.user.userprofile.save()
        cls.admin = User.objects.create_superuser(
            'admin1@example.com', 'admin1')

    def setUp(self):
        self.user_client = APIClient()
        self.user_authorized_client = APIClient()
        self.user_authorized_client.force_authenticate(
            CatalogueViewsTests.user)
        self.admin_client = APIClient()
        self.admin_client.force_login(CatalogueViewsTests.admin)

    # def test_update_db(self):
    #     """Загрузка полной БД с WB по API """
    #     address = '/api/update/'
    #     response = self.admin_client.get(address)
    #     print(response.status_code)
    #     print(response.data)
    #     self.assertEqual(response.status_code, HTTPStatus.OK,)

    def test_user_get_list_products_filtered_by_category(self):
        """
        получение списка товаров c фильтром по
        категории category=1 с учетом товаров в подкатегории
        """
        address = '/api/catalogue/?category=1'
        response = self.user_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(3, products_count,
                         'Пользователь не получил товары'
                         ' из подкатегорий')

    def test_list_products_filtered_by_category_without_sub_category(self):
        """
        получение списка товаров c фильтром по
        категории category=1 без учетом товаров в подкатегории
        """
        address = '/api/catalogue/?category=1&sub_category=false'
        response = self.user_client.get(address)
        products_count = len(response.data.get('results'))

        self.assertEqual(1, products_count,
                         'Пользователь получил товары'
                         'из подкатегорий')

    def test_products_search(self):
        """
        поиск товаров по наименованию
        """
        address = '/api/catalogue/?search=поиск'
        response = self.user_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(1, products_count,
                         'Пользователь получил товары'
                         'из подкатегорий')

    def test_products_search_in_description(self):
        """
        поиск товаров по наименованию и описанию
        """
        address = ('/api/catalogue/?search='
                   'description%20search&description=true')
        response = self.user_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(1, products_count,
                         'Не найден товар по фразе из описания')

    def test_common_search(self):
        """
        поиск товаров по наименованию
        """
        address = '/api/search/?search=ка'
        response = self.user_client.get(address)
        category_count = len(response.data.get('category'))
        self.assertEqual(2, category_count,
                         'Пользователь не получил'
                         ' категорий')
        products_count = len(response.data.get('product').get('results'))
        self.assertEqual(3, products_count,
                         'Пользователь не получил товары')

    def test_search_in_description_(self):
        """
        поиск товаров по наименованию и описанию
        """
        address = ('/api/search/?search='
                   'description%20search&description=true')
        response = self.user_client.get(address)
        products_count = len(response.data.get('product').get('results'))
        self.assertEqual(1, products_count,
                         'Не найден товар по фразе из описания')

    def test_products_search_in_category_without_sub_category(self):
        """
        поиск товаров по наименованию среди товаров определенной
        категории, без учета товаров в подкатегории
        """
        address = '/api/catalogue/?category=1&sub_category=false&search=поиск'
        response = self.user_client.get(address)
        products_count = len(response.data.get('results'))

        self.assertEqual(0, products_count,
                         'Пользователь получил товары'
                         'из подкатегорий')

    def test_user_get_list_categories(self):
        """получение списка категорий"""
        address = '/api/catalogue/category/'
        response = self.user_client.get(address)
        categories_count = len(response.data)
        self.assertEqual(3, categories_count,
                         'Пользователь получил категории'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'id': 4,
                'name': 'Категория1',
                'slug': 'kategoriya1',
                'branches': [],
                'root': 'Подкатегория',
                'is_prohibited': False,
                'is_visible_on_main': True
            },
            {
                'id': 1,
                'name': 'Корневая категория',
                'slug': 'kornevaya-kategoriya',
                'branches': ['Подкатегория'],
                'root': None,
                'is_prohibited': False,
                'is_visible_on_main': False
            },
            {
                'id': 3,
                'name': 'Подкатегория',
                'slug': 'podkategoriya',
                'branches': ['Категория1'],
                'root': 'Корневая категория',
                'is_prohibited': False,
                'is_visible_on_main': False
            }
        ]
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_search_category(self):
        """поиск категорий по имени"""
        address = '/api/catalogue/category/?search=Подкат'
        response = self.user_client.get(address)
        categories_count = len(response.data)
        self.assertEqual(1, categories_count,
                         'Не найдена категория')

    def test_user_get_list_filtered_tree_category(self):
        """получение категорий с параметром tree_category"""
        address = '/api/catalogue/category/?category_tree=true'
        response = self.user_client.get(address)
        categories_count = len(response.data)
        self.assertEqual(1, categories_count,
                         'Пользователь получил категории'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'id': 1,
                'name': 'Корневая категория',
                'slug': 'kornevaya-kategoriya',
                'branches': [
                    {
                        'id': 3,
                        'name': 'Подкатегория',
                        'slug': 'podkategoriya',
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
                'root': None,
                'is_prohibited': False,
                'is_visible_on_main': False
            }
        ]
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_list_category_filtered_is_visible_on_main(self):
        """получение категорий с параметром is_visible_on_main"""
        address = '/api/catalogue/category/?is_visible_on_main=true'
        response = self.user_client.get(address)
        categories_count = len(response.data)
        self.assertEqual(1, categories_count,
                         'Пользователь получил категории'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'id': 4,
                'name': 'Категория1',
                'slug': 'kategoriya1',
                'branches': [],
                'root': 'Подкатегория',
                'is_prohibited': False,
                'is_visible_on_main': True
            }
        ]
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_item_category(self):
        """получение отдельной категории"""
        category = CatalogueViewsTests.category
        address = f'/api/catalogue/category/{category.slug}/'
        response = self.user_client.get(address)
        expected_data = {
            'id': 4,
            'name': 'Категория1',
            'slug': 'kategoriya1',
            'branches': [],
            'root': 'Подкатегория',
            'is_prohibited': False,
            'is_visible_on_main': True
        }
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_list_brands(self):
        """получение списка производителей"""
        address = '/api/catalogue/brand/'
        response = self.user_client.get(address)
        brands_count = len(response.data)
        self.assertEqual(2, brands_count,
                         'Пользователь получил бренды'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'id': 1,
                'name': 'Бренд',
                'slug': 'brend',
                'image': 'http://testserver/media/brand-images/'
                         'brend/logo_brand.gif',
                'is_prohibited': False,
                'is_visible_on_main': False
            }
        ]
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_list_brands_is_visible_on_main(self):
        """
        получение списка производителей, которые должны
        быть на главной странице
        """
        address = '/api/catalogue/brand/?is_visible_on_main=false'
        response = self.user_client.get(address)
        brands_count = len(response.data)
        self.assertEqual(1, brands_count,
                         'Пользователь получил бренды'
                         ' непредназначенные для публикации')

    def test_user_get_item_brand(self):
        """получение отдельного производителя"""
        brand = CatalogueViewsTests.brand
        address = f'/api/catalogue/brand/{brand.slug}/'
        response = self.user_client.get(address)
        expected_data = {
            'id': 1,
            'name': 'Бренд',
            'slug': 'brend',
            'image': 'http://testserver/media/brand-images/'
                     'brend/logo_brand.gif',
            'is_prohibited': False,
            'is_visible_on_main': False
        }
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_get_list_products(self):
        """получение списка товаров"""
        address = '/api/catalogue/'
        price = round(CatalogueViewsTests.product.price * 0.8, 2)
        response = self.user_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(3, products_count,
                         'Пользователь получил товары'
                         ' непредназначенные для публикации')
        expected_data = [
            {
                'id': 1,
                'category': 'Категория1',
                'brand': 'Бренд',
                'images': [
                    {
                        'image': (
                            'http://testserver/media/'
                            'product-images/'
                            'puskovoe-zaryadnoe-ustrojstvo-2'
                            '-dlya-poiska-169110394/'
                            'prod_img.gif'
                        )
                    }
                ],
                'price': price,
                'name': 'Пусковое зарядное устройство 2 для поиска',
                'slug': 'puskovoe-zaryadnoe-ustrojstvo-2'
                        '-dlya-poiska-169110394',
                'description': 'Хороший продукт для description search',
                'code': 169110394,
                'wb_urls': 'https://www.wildberries.ru/'
                           'catalog/169110394/detail.aspx',
                'quantity': 999999.0,
                'is_deleted': False
            },
            {
                'id': 3,
                'category': 'Корневая категория',
                'brand': 'Бренд',
                'images': [],
                'price': price,
                'name': 'Пусковое зарядное устройство 4',
                'slug': 'puskovoe-zaryadnoe-ustrojstvo-4-1691103959',
                'description': 'Хороший продукт для 4',
                'code': 1691103959,
                'wb_urls': 'https://www.wildberries.ru/'
                           'catalog/1691103959/detail.aspx',
                'quantity': 999999.0,
                'is_deleted': False
            },
            {
                'id': 4,
                'category': 'Подкатегория',
                'brand': 'Бренд',
                'images': [],
                'price': price,
                'name': 'Пусковое зарядное устройство 5',
                'slug': 'puskovoe-zaryadnoe-ustrojstvo-5-1691103945',
                'description': 'Хороший продукт для',
                'code': 1691103945,
                'wb_urls': 'https://www.wildberries.ru/'
                           'catalog/1691103945/detail.aspx',
                'quantity': 999999.0,
                'is_deleted': False
            }
        ]
        self.check_fields(response=response.data.get(
            'results'), expected_data=expected_data)

    def test_user_get_item_product(self):
        """получение товара цена со скидкой 20%"""
        product = CatalogueViewsTests.product
        price = round(product.price * 0.8, 2)
        address = f'/api/catalogue/{product.slug}/'
        response = self.user_client.get(address)
        expected_data = {
            'id': 1,
            'category': 'Категория1',
            'brand': 'Бренд',
            'images': [
                {
                    'image': 'http://testserver/media/'
                             'product-images/'
                             'puskovoe-zaryadnoe-ustrojstvo-2'
                             '-dlya-poiska-169110394/'
                             'prod_img.gif'
                }
            ],
            'price': price,
            'name': 'Пусковое зарядное устройство 2 для поиска',
            'slug': 'puskovoe-zaryadnoe-ustrojstvo-2-dlya-poiska-169110394',
            'description': 'Хороший продукт для description search',
            'code': 169110394,
            'wb_urls': 'https://www.wildberries.ru/'
                       'catalog/169110394/detail.aspx',
            'quantity': 999999.0,
            'is_deleted': False,
            'label_hit': False,
            'label_popular': False
        }
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_authorized_get_item_product(self):
        """получение товара цена со скидкой 50%"""
        product = CatalogueViewsTests.product
        price = round(product.price * 0.5, 2)
        address = f'/api/catalogue/{product.slug}/'
        response = self.user_authorized_client.get(address)
        expected_data = {
            'id': 1,
            'category': 'Категория1',
            'brand': 'Бренд',
            'images': [
                {
                    'image': 'http://testserver/media/'
                             'product-images/'
                             'puskovoe-zaryadnoe-ustrojstvo-2'
                             '-dlya-poiska-169110394/'
                             'prod_img.gif'
                }
            ],
            'price': price,
            'name': 'Пусковое зарядное устройство 2 для поиска',
            'slug': 'puskovoe-zaryadnoe-ustrojstvo-2-dlya-poiska-169110394',
            'description': 'Хороший продукт для description search',
            'code': 169110394,
            'wb_urls': 'https://www.wildberries.ru/'
                       'catalog/169110394/detail.aspx',
            'quantity': 999999.0,
            'is_deleted': False
        }
        self.check_fields(response=response.data, expected_data=expected_data)

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

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
