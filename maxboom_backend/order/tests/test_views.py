import shutil
import tempfile
from decimal import Decimal
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from cart.models import Cart, ProductCart
from catalogue.models import Product, ProductImage
from order.models import Commodity, Order

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderViewsTests(TestCase):
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
        cls.product = Product.objects.create(
            name='Овощерезка',
            description='Хороший продукт',
            price=180,
            code=169110584,
            vendor_code='артикул овощерезки',
            is_deleted=False,
        )
        cls.product_grater = Product.objects.create(
            name='Терка',
            description='Хороший продукт',
            price=18,
            code=169110984,
            vendor_code='артикул терки',
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
        cls.user = User.objects.create_user(
            'test_user@example.com', 'test_pass')
        cls.userprofile = cls.user.userprofile
        cls.userprofile.is_vendor = True
        cls.userprofile.save()

        cls.order_user = Order.objects.create(
            user=cls.user,
            phone='+79991243584',
            email=cls.user.email,
            address='г.Москва, ул. Ленина, д. 41, к. 2'
        )
        cls.commodity = Commodity.objects.create(
            product=cls.product,
            quantity=3,
            order=cls.order_user
        )
        cls.cart = Cart.objects.create(
            user=cls.user,
            is_active=True,
        )
        cls.product_cart = ProductCart.objects.create(
            cart=cls.cart,
            product=cls.product,
            amount=10
        )
        cls.user_without_cart = User.objects.create(
            email='mm@mm.mm',
            password='123456'
        )

    def setUp(self):
        self.anonym_client = APIClient()
        self.anonym_client_with_cart = APIClient()
        self.user_client = APIClient()
        self.user_authorized_client = APIClient()
        self.user_authorized_client.force_authenticate(
            OrderViewsTests.user)
        self.client_without_cart = APIClient()
        self.client_without_cart.force_authenticate(
            OrderViewsTests.user_without_cart
        )

    def test_anonym_client_with_cart_post_order(self):
        """Проверка значений полей анонимный клиент c корзиной"""
        client = APIClient()
        data_cart = {
            'product': 1,
            'amount': 10,
        }
        response = client.post('/api/cart/', data_cart)
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        resp = client.get('/api/cart/')
        self.assertEquals(resp.status_code, HTTPStatus.OK)
        data_order = {
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'phone': '+79991243584',
            'email': 'ww@fsf.et',
            'comment': 'Срочно',
        }
        expected_data = {
            'user': None,
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'phone': '+79991243584',
            'email': 'ww@fsf.et',
            'comment': 'Срочно',
            'value': 1440,
            'commodities': [
                {
                    'name': 'Овощерезка',
                    'image': ('http://testserver/media/product-images/'
                              'ovoscherezka-169110584/prod_img.gif'),
                    'quantity': 10,
                    'price': 144,
                    'code': 169110584,
                    'product': 1
                }
            ],
            'is_paid': False
        }
        response = client.post('/api/order/', data=data_order)
        self.assertEquals(
            response.status_code, HTTPStatus.CREATED,
            'Несоответствие кода ответа при создании заказа'
        )
        self.check_fields(response=response.data, expected_data=expected_data)
        response = client.post('/api/order/', data=data_order)
        self.assertEquals(
            response.status_code, HTTPStatus.BAD_REQUEST,
            'Не создавать заказ с пустой корзиной'
        )
        product_grater = OrderViewsTests.product_grater
        data_change = {
            'commodities': [
                {
                    'quantity': 9,
                    'product': 1
                },
                {
                    'product': product_grater.id,
                    'quantity': 1,
                }
            ]
        }
        response = client.patch('/api/order/2/', data=data_change)
        self.assertEquals(
            response.status_code, HTTPStatus.METHOD_NOT_ALLOWED,
            'Не соответствие кода ответа при обновлении заказа'
        )
        expected_put = {
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'phone': '+79991243584', 'email': 'ww@fsf.et',
            'comment': 'Замена',
            'commodities': [
                {
                    'quantity': 8,
                    'product': 1
                },
                {
                    'quantity': 2,
                    'product': 2
                }
            ]
        }
        response = client.put('/api/order/2/', data=expected_put)
        self.assertEquals(
            response.status_code, HTTPStatus.METHOD_NOT_ALLOWED,
            'Не соответствие кода ответа при запрещенном методе'
        )

    def test_anonym_client_without_cart_post_order(self):
        """Проверка значений полей анонимный клиент без корзины"""
        data_order = {
            'user': 1,
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'phone': '+79991243584',
            'email': 'ww@fsf.et',
            'comment': 'Срочно',
        }
        client = self.anonym_client
        response = client.post('/api/order/', data=data_order)
        self.assertEquals(response.status_code, HTTPStatus.BAD_REQUEST)
        response = client.get('/api/order/')
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(
            len(response.data), 0,
            'Получены заказы не предназначенные пользователю'
        )

    def test_user_get_order(self):
        """Проверка соответствия значений полей get-запрос"""
        user = self.user_authorized_client
        response = user.get('/api/order/')
        expected_data = [
            {
                'user': 1,
                'session_id': None,
                'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
                'phone': '+79991243584',
                'email': 'test_user@example.com',
                'comment': None,
                'value': 270,
                'commodities': [
                    {
                        'name': 'Овощерезка',
                        'image': ('http://testserver/media/product-images/'
                                  'ovoscherezka-169110584/prod_img.gif'),
                        'quantity': 3,
                        'price': 90,
                        'code': 169110584
                    }
                ]
            }
        ]
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_post_order(self):
        """Проверка значений полей post-запрос"""
        client = self.user_authorized_client
        data_order = {
            'user': 1,
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'phone': '+79991243584',
            'comment': 'Срочно',
        }
        expected_data = {
            'user': 1,
            'session_id': None,
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'phone': '+79991243584',
            'email': 'test_user@example.com',
            'comment': 'Срочно',
            'value': 900.0,
            'commodities': [
                {
                    'name': 'Овощерезка',
                    'image': ('http://testserver/media/product-images/'
                              'ovoscherezka-169110584/prod_img.gif'),
                    'quantity': 10,
                    'price': 90.0,
                    'code': 169110584
                }
            ]
        }
        response = client.post('/api/order/', data=data_order)
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        self.check_fields(response=response.data, expected_data=expected_data)

    def test_user_patch_order(self):
        """Проверка значений полей patch-запрос"""
        user = self.user_authorized_client
        data_order = {
            'phone': '+79991243585',
            'comment': 'Уменьшить количество',
            'commodities': [
                {
                    'quantity': 2,
                    'product': 1
                }
            ]
        }
        response = user.patch('/api/order/1/', data=data_order,)
        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_user_refund_order(self):
        user = User.objects.create_user('tet@tt.tu', '12345')
        cli = APIClient()
        cli.force_authenticate(user)
        data_cart = {
            'product': 2,
            'amount': 10,
        }
        resp = cli.post('/api/cart/', data=data_cart)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        data_order = {
            'user': 1,
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'phone': '+79991243584',
            'comment': 'Срочно',
        }
        resp = cli.post('/api/order/', data=data_order)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        data_refund = {
            'commodities': [
                {'commodity': 2,
                 'quantity': 2
                 },
            ]
        }
        resp = cli.post('/api/order/1/refund/', data=data_refund)
        self.assertEqual(
            resp.status_code, HTTPStatus.FORBIDDEN,
            ('Нельзя оформлять возврат для заказа,'
             ' не принадлежащего пользователю')
        )
        resp = cli.post('/api/order/2/refund/', data=data_refund)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        expected_data = {
            'id': 1,
            'order': 2,
            'commodities': [
                {
                    'id': 1,
                    'name': 'Терка',
                    'image': None,
                    'price': Decimal('14.400'),
                    'code': 169110984,
                    'commodity': 2,
                    'quantity': 2
                }
            ],
            'value': Decimal('28.800'),
            'is_refunded': False
        }
        self.check_fields(response=resp.data, expected_data=expected_data)
        data_refund = {
            'commodities': [
                {'commodity': 2,
                 'quantity': 9
                 },
            ]
        }
        resp = cli.post('/api/order/2/refund/', data=data_refund)
        self.assertEqual(
            resp.status_code, HTTPStatus.BAD_REQUEST,
            'Нельзя возвратить больше товара, чем осталось в заказе'
        )
        data_refund = {
            'commodities': [
                {'commodity': 1,
                 'quantity': 9
                 },
            ]
        }
        resp = cli.post('/api/order/2/refund/', data=data_refund)
        self.assertEqual(
            resp.status_code, HTTPStatus.BAD_REQUEST,
            'Нельзя возвратить товар, которого нет в заказе'
        )

    def test_user_cancel_order(self):
        user = User.objects.create_user('tet@tt.tu', '12345')
        cli = APIClient()
        cli.force_authenticate(user)
        data_cart = [
            {
                'product': 2,
                'amount': 10,
            },
            {
                'product': 1,
                'amount': 2,
            },
        ]
        for data in data_cart:
            resp = cli.post('/api/cart/', data=data)
            self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                             'Не создана корзина')
        data_order = {
            'user': 1,
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'phone': '+79991243584',
            'comment': 'Срочно',
        }
        resp = cli.post('/api/order/', data=data_order)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                         'Не создан заказ')
        self.assertEqual(resp.data.get('status'), 'создан')
        order_id = resp.data.get('id')
        resp = cli.post(f'/api/order/{order_id}/cancel/')
        self.assertEqual(resp.status_code, HTTPStatus.OK,
                         'Не удалось отменить заказ')
        self.assertEqual(resp.data.get('status'), 'отменен')
        resp = cli.post(f'/api/order/{order_id}/cancel/')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST,
                         'Повторная отмена невозможна')
        data_cart = [
            {
                'product': 2,
                'amount': 10,
            },
            {
                'product': 1,
                'amount': 2,
            },
        ]
        for data in data_cart:
            resp = cli.post('/api/cart/', data=data)
            self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                             'Не создана корзина')
        resp = cli.post('/api/order/', data=data_order)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                         'Не создан заказ')
        order_id = resp.data.get('id')
        commodity_id = resp.data.get('commodities')[0].get('id')
        data_refund = {
            'commodities': [
                {'commodity': commodity_id,
                 'quantity': 1
                 },
            ]
        }
        resp = cli.post(f'/api/order/{order_id}/refund/', data=data_refund)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                         'Не создан частичный возврат')
        resp = cli.post(f'/api/order/{order_id}/cancel/')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST,
                         'Частичная отмена заказа невозможна')
        order_id = Order.objects.exclude(user=user)[0].id
        resp = cli.post(f'/api/order/{order_id}/cancel/')
        self.assertEqual(
            resp.status_code, HTTPStatus.FORBIDDEN,
            ('Нельзя оформлять отмену для заказа,'
             ' не принадлежащего пользователю')
        )

    def test_anonym_cancel_order(self):
        cli = APIClient()
        data_cart = [
            {
                'product': 2,
                'amount': 10,
            },
            {
                'product': 1,
                'amount': 2,
            },
        ]
        for data in data_cart:
            resp = cli.post('/api/cart/', data=data)
            self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                             'Не создана корзина')
        data_order = {
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
            'email': 'mm@mm.mm',
            'phone': '+79991243584',
            'comment': 'Срочно',
        }
        resp = cli.post('/api/order/', data=data_order)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                         'Не создан заказ')
        self.assertEqual(resp.data.get('status'), 'создан')
        order_id = resp.data.get('id')
        session_id = resp.data.get('session_id')
        resp = cli.post(f'/api/order/{order_id}/cancel/')
        self.assertEqual(resp.status_code, HTTPStatus.OK,
                         'Не удалось отменить заказ')
        self.assertEqual(resp.data.get('status'), 'отменен')
        resp = cli.post(f'/api/order/{order_id}/cancel/')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST,
                         'Повторная отмена невозможна')
        data_cart = [
            {
                'product': 2,
                'amount': 10,
            },
            {
                'product': 1,
                'amount': 2,
            },
        ]
        for data in data_cart:
            resp = cli.post('/api/cart/', data=data)
            self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                             'Не создана корзина')
        resp = cli.post('/api/order/', data=data_order)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                         'Не создан заказ')
        order_id = resp.data.get('id')
        commodity_id = resp.data.get('commodities')[0].get('id')
        data_refund = {
            'commodities': [
                {'commodity': commodity_id,
                 'quantity': 1
                 },
            ]
        }
        resp = cli.post(f'/api/order/{order_id}/refund/', data=data_refund)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED,
                         'Не создан частичный возврат')
        resp = cli.post(f'/api/order/{order_id}/cancel/')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST,
                         'Частичная отмена заказа невозможна')
        order_id = Order.objects.exclude(session_id=session_id)[0].id
        self.assertEqual(
            resp.status_code, HTTPStatus.BAD_REQUEST,
            ('Нельзя оформлять отмену для заказа,'
             ' не принадлежащего пользователю')
        )

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
