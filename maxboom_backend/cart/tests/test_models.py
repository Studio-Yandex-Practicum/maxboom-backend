# flake8: noqa
import tempfile
import shutil
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from catalogue.models import Product, ProductImage, Brand, Category
from cart.models import Cart, ProductCart


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CartTestCase(TestCase):

    user_data = {
        'email': 'test_example@test',
        'password': 'testpassword1',
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            **cls.user_data
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
        )
        cls.cart = Cart.objects.create(
            user=cls.user,
            is_active=True,
        )
        cls.product_1_cart = ProductCart.objects.create(
            cart=cls.cart,
            product=cls.product_1,
            amount=10,
        )

    def test_model_exists(self):
        carts_count = Cart.objects.count()
        expected_count = 1
        self.assertEqual(carts_count, expected_count)

    def test_cannot_duplicate_user_cart(self):
        with transaction.atomic():
            try:
                Cart.objects.create(
                    user=CartTestCase.user,
                    is_active=True,
                )
            except Exception as e:
                self.assertEqual(type(e), IntegrityError)
        carts_count = Cart.objects.count()
        expected_count = 1
        self.assertEqual(carts_count, expected_count)

    def test_correct_user_cart_representation(self):
        cart = Cart.objects.all()[0]
        expected_representation = f"Корзина пользователя: {CartTestCase.user}"
        self.assertEqual(str(cart), expected_representation)

    def test_create_anonymous_cart(self):
        session = str(uuid.uuid4())
        Cart.objects.create(
            session_id=session,
            is_active=False,
        )
        carts_count = Cart.objects.count()
        expected_count = 2
        self.assertEqual(carts_count, expected_count)

    def test_correct_anonymous_cart_representation(self):
        session = str(uuid.uuid4())
        Cart.objects.create(
            session_id=session,
            is_active=False,
        )
        cart = Cart.objects.all()[1]
        expected_representation = f"Корзина пользователя: {None}"
        self.assertEqual(str(cart), expected_representation)

    def test_cart_product_access(self):
        cart = Cart.objects.all()[0]
        product = CartTestCase.product_1_cart
        cart_products = cart.products
        self.assertEqual(cart_products.all()[0], product.product)

    def test_cart_full_price(self):
        cart = CartTestCase.cart
        product_price = 100
        product_amount = 10
        expected_full_price = round(product_price * product_amount, 2)
        self.assertEqual(cart.cart_full_price, expected_full_price)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProductCartTestCase(TestCase):

    user_data = {
        'email': 'test_example@test',
        'password': 'testpassword1',
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            **cls.user_data
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
        )
        cls.cart = Cart.objects.create(
            user=cls.user,
            is_active=True,
        )
        cls.product_1_cart = ProductCart.objects.create(
            cart=cls.cart,
            product=cls.product_1,
            amount=10,
        )

    def test_model_exists(self):
        product_carts_count = ProductCart.objects.count()
        expected_count = 1
        self.assertEqual(product_carts_count, expected_count)

    def test_cannot_duplicate_product_carts(self):
        with transaction.atomic():
            try:
                ProductCart.objects.create(
                    product=ProductCartTestCase.product_1,
                    cart=ProductCartTestCase.cart,
                    amount=20,
                )
            except Exception as e:
                self.assertEqual(type(e), IntegrityError)
        product_carts_count = ProductCart.objects.count()
        expected_count = 1
        self.assertEqual(product_carts_count, expected_count)

    def test_create_product_cart_object(self):
        product_2 = Product.objects.create(
            name='test_product_2',
            description='Test product 2 description',
            price=200,
            brand=ProductCartTestCase.brand_1,
            category=ProductCartTestCase.cat_1,
            code=987654321,
            vendor_code='article_2',
            wb_urls='https://www.test_url.test2',
            is_deleted=True,
        )
        ProductCart.objects.create(
            cart=ProductCartTestCase.cart,
            product=product_2,
            amount=20,
        )
        product_cart_count = ProductCart.objects.count()
        expected_count = 2
        self.assertEqual(product_cart_count, expected_count)
        cart_products = CartTestCase.cart.products.all()
        self.assertEqual(product_2, cart_products[1])

    def test_correct_user_product_cart_representation(self):
        product_cart = ProductCart.objects.all()[0]
        product = Product.objects.all()[0]
        expected_representation = f"Продукт {product} в корзине пользователя: {CartTestCase.user}"
        self.assertEqual(str(product_cart), expected_representation)

    def test_create_anonymous_product_cart(self):
        session = str(uuid.uuid4())
        new_cart = Cart.objects.create(
            session_id=session,
            is_active=False,
        )
        ProductCart.objects.create(
            product=ProductCartTestCase.product_1,
            cart=new_cart,
            amount=20,
        )
        product_carts_count = ProductCart.objects.count()
        expected_count = 2
        self.assertEqual(product_carts_count, expected_count)

    def test_correct_anonymous_cart_representation(self):
        session = str(uuid.uuid4())
        new_cart = Cart.objects.create(
            session_id=session,
            is_active=False,
        )
        ProductCart.objects.create(
            product=ProductCartTestCase.product_1,
            cart=new_cart,
            amount=20,
        )
        product_cart = ProductCart.objects.all()[1]
        product = Product.objects.all()[0]
        expected_representation = f"Продукт {product} в корзине пользователя: {None}"
        self.assertEqual(str(product_cart), expected_representation)

    def test_product_cart_access(self):
        cart = Cart.objects.all()[0]
        product_cart = ProductCartTestCase.product_1_cart
        self.assertEqual(product_cart.cart, cart)

    def test_product_cart_full_price(self):
        product_cart = CartTestCase.product_1_cart
        product_price = 100
        product_amount = 10
        expected_full_price = round(product_price * product_amount, 2)
        self.assertEqual(product_cart.full_price, expected_full_price)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
