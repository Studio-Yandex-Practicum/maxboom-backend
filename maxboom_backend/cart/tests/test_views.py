# flake8: noqa
import tempfile
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from catalogue.models import Product, ProductImage, Brand, Category
from cart.models import Cart, ProductCart


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CartViewsTestCase(TestCase):

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
    user_data = {
        'email': 'test_example@test',
        'password': 'testpassword1',
    }
    superuser_data = {
        'email': 'test@test.test',
        'password': 'test',
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            **cls.user_data
        )
        cls.superuser = User.objects.create_superuser(
            **cls.superuser_data
        )
        cls.brand_1 = Brand.objects.create(
            name='test_brand_1',
            slug='testbrand',
        )
        cls.cat_1 = Category.objects.create(
            name='test_category_1',
            slug='testcat1',
            wb_category_id=12345
        )
        cls.product_1 = Product.objects.create(
            name='test_product_1',
            description='Test product description',
            price=100,
            brand=cls.brand_1,
            category=cls.cat_1,
            code=123456789,
            vendor_code='article_1',
            wb_urls='https://www.test_url.test',
            is_deleted=True,
            weight=1.45
        )
        cls.product_1_image = ProductImage.objects.create(
            product=cls.product_1,
            image=cls.image
        )
        cls.cart = Cart.objects.create(
            user=cls.user,
            is_active=True,
            session_id=None,
        )
        cls.product_1_cart = ProductCart.objects.create(
            cart=cls.cart,
            product=cls.product_1,
            amount=10,
        )
        cls.cart_2 = Cart.objects.create(
            user=cls.superuser,
            is_active=True,
            session_id=None,
        )
        cls.product_2_cart = ProductCart.objects.create(
            cart=cls.cart_2,
            product=cls.product_1,
            amount=10,
        )

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.force_login(user=self.superuser)

    def test_get_cart_anonymous_viewset(self):
        url = '/api/cart/'
        response = self.client.get(url)
        expected_data = {
            'id': 3,
            'products': [],
            'user': None,
            'cart_full_price': 0,
            'cart_full_weight': 0
        }
        response_data = response.data
        self.assertEqual(response_data, expected_data)

    def test_get_cart_authorized_viewset(self):
        url = '/api/cart/'
        image_url = 'http://testserver'
        image = CartViewsTestCase.product_1.images.all()[0].image.url
        response = self.admin_client.get(url)
        expected_data = {
            'id': 2,
            'products': [
                {
                    'product': {
                        'id': 1,
                        'category': 'test_category_1',
                        'brand': 'test_brand_1',
                        'images': [
                            {
                                'image': image_url + image
                            }
                        ],
                        'price': 80.0,
                        'name': 'test_product_1',
                        'slug': 'testproduct1-123456789',
                        'description': 'Test product description',
                        'code': 123456789,
                        'wb_urls': 'https://www.test_url.test',
                        'quantity': 999999.0,
                        'is_deleted': True,
                        'wholesale': 0,
                        'label_hit': False,
                        'label_popular': False,
                        'weight': '1.450'
                    },
                    'amount': 10,
                    'full_price': 800.0,
                    'full_weight': 14.5
                }
            ],
            'user': 2,
            'cart_full_price': 800.0,
            'cart_full_weight': 14.5
        }
        self.assertEqual(response.data, expected_data)

    def test_post_cart_anonymous_viewset(self):
        url = '/api/cart/'
        data = {
            'product': 1,
            'amount': 10,
        }
        response = self.client.post(url, data)
        expected_data = {
            'product': 1,
            'cart': 3,
            'amount': 10,
        }
        self.assertEqual(response.data, expected_data)
        carts_count = Cart.objects.count()
        expected_count = 3
        self.assertEqual(carts_count, expected_count)
        product_carts_count = ProductCart.objects.count()
        expected_count = 3
        self.assertEqual(product_carts_count, expected_count)

    def test_add_to_cart(self):
        url = '/api/cart/'
        data = {
            'product': 1,
            'amount': 10,
        }
        self.client.post(url, data)
        response = self.client.post(url, data)
        expected_data = {
            'product': 1,
            'cart': 3,
            'amount': 20,
        }
        self.assertEqual(response.data, expected_data)
        product_cart_count = ProductCart.objects.count()
        expected_count = 3
        self.assertEqual(product_cart_count, expected_count)

    def test_increase_product_by_one(self):
        add_url = '/api/cart/add/'
        cart_url = '/api/cart/'
        image_url = 'http://testserver'
        image = CartViewsTestCase.product_1.images.all()[0].image.url
        data = {
            'product': 1,
        }
        self.admin_client.put(add_url, data)
        response = self.admin_client.get(cart_url)
        expected_data = {
            'id': 2,
            'products': [
                {
                    'product': {
                        'id': 1,
                        'category': 'test_category_1',
                        'brand': 'test_brand_1',
                        'images': [
                            {
                                'image':  image_url + image
                            }
                        ],
                        'price': 80.0,
                        'name': 'test_product_1',
                        'slug': 'testproduct1-123456789',
                        'description': 'Test product description',
                        'code': 123456789,
                        'wb_urls': 'https://www.test_url.test',
                        'quantity': 999999.0,
                        'is_deleted': True,
                        'wholesale': 0,
                        'label_hit': False,
                        'label_popular': False,
                        'weight': '1.450'
                    },
                    'amount': 11,
                    'full_price': 880.00,
                    'full_weight': 15.95
                }
            ],
            'user': 2,
            'cart_full_price': 880.00,
            'cart_full_weight': 15.95
        }
        self.assertEqual(response.data, expected_data)

    def test_decrease_product_by_one(self):
        dec_url = '/api/cart/subtract/'
        cart_url = '/api/cart/'
        image_url = 'http://testserver'
        image = CartViewsTestCase.product_1.images.all()[0].image.url
        data = {
            'product': 1,
        }
        self.admin_client.put(dec_url, data)
        response = self.admin_client.get(cart_url)
        expected_data = {
            'id': 2,
            'products': [
                {
                    'product': {
                        'id': 1,
                        'category': 'test_category_1',
                        'brand': 'test_brand_1',
                        'images': [
                            {
                                'image':  image_url + image
                            }
                        ],
                        'price': 80.0,
                        'name': 'test_product_1',
                        'slug': 'testproduct1-123456789',
                        'description': 'Test product description',
                        'code': 123456789,
                        'wb_urls': 'https://www.test_url.test',
                        'quantity': 999999.0,
                        'is_deleted': True,
                        'wholesale': 0,
                        'label_hit': False,
                        'label_popular': False,
                        'weight': '1.450'
                    },
                    'amount': 9,
                    'full_price': 720.0,
                    'full_weight': 13.05
                }
            ],
            'user': 2,
            'cart_full_price': 720.0,
            'cart_full_weight': 13.05
        }
        self.assertEqual(response.data, expected_data)

    def tearDown(self):
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
