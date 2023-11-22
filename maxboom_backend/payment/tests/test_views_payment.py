"""Для успешного прохождения теста .env должен содержать
: Y_SECRET_KEY=*** Y_SHOP_ID=***.
Тест выполняется вручную, т.к. необходимо выполнить
подтверждение оплаты на стороне yookassa по ссылке
url = client.post(
    f'/api/order/{order_id}/payment/').data.get(
        'confirmation_url')
"""
# import re
# import shutil
# import tempfile
# from http import HTTPStatus

# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import TestCase, override_settings
# from rest_framework.test import APIClient
# from yookassa import Payment

# from cart.models import Cart, ProductCart
# from catalogue.models import Product, ProductImage
# from order.models import Commodity, CommodityRefund, Order, OrderRefund
# from payment.models import OrderPayment, Repayment

# User = get_user_model()

# TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# @override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
# class PaymentViewsTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.small_gif = (
#             b'\x47\x49\x46\x38\x39\x61\x02\x00'
#             b'\x01\x00\x80\x00\x00\x00\x00\x00'
#             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
#             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
#             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
#             b'\x0A\x00\x3B'
#         )
#         cls.product = Product.objects.create(
#             name='Овощерезка',
#             description='Хороший продукт',
#             price=180,
#             code=169110584,
#             vendor_code='артикул овощерезки',
#             is_deleted=False,
#         )
#         cls.product_grater = Product.objects.create(
#             name='Терка',
#             description='Хороший продукт',
#             price=18,
#             code=169110984,
#             vendor_code='артикул терки',
#             is_deleted=False,
#         )
#         cls.uploaded = SimpleUploadedFile(
#             name='prod_img.gif',
#             content=cls.small_gif,
#             content_type='image/gif'
#         )
#         cls.image = ProductImage.objects.create(
#             product=cls.product,
#             image=cls.uploaded
#         )
#         cls.user = User.objects.create_user(
#             'test_user@example.com', 'test_pass')
#         cls.user_vendor = User.objects.create_user(
#             'test_user_v@example.com', 'test_pass')
#         cls.user_vendor.profile.is_vendor = True
#         cls.user_vendor.profile.save()
#         cls.order_user = Order.objects.create(
#             user=cls.user,
#             phone='+79991243584',
#             email=cls.user.email,
#             address='г.Москва, ул. Ленина, д. 41, к. 2'
#         )
#         cls.order_user_v = Order.objects.create(
#             user=cls.user_vendor,
#             phone='+79991243584',
#             address='г.Москва, ул. Ленина, д. 41, к. 2'
#         )
#         cls.commodity = Commodity.objects.create(
#             product=cls.product,
#             quantity=10,
#             order=cls.order_user_v
#         )
#         cls.commodity = Commodity.objects.create(
#             product=cls.product,
#             quantity=10,
#             order=cls.order_user
#         )
#         cls.cart = Cart.objects.create(
#             user=cls.user,
#             is_active=True,
#         )
#         cls.product_cart = ProductCart.objects.create(
#             cart=cls.cart,
#             product=cls.product,
#             amount=12
#         )
#         cls.user_without_cart = User.objects.create(
#             email='mm@mm.mm',
#             password='123456'
#         )
#         cls.payment = OrderPayment.objects.create(
#             order=cls.order_user_v,
#             payment_id='2cdedfd4-000f-5000-8000-1be0be5d3862',
#         )
#         cls.payment_u = OrderPayment.objects.create(
#             idempotence_key='a2aba011-89b8-48f2-a13c-fd2453616215',
#             order=cls.order_user,
#             payment_id='2ced5f29-000f-5000-9000-1a902705317e'
#         )

#     def setUp(self):
#         self.anonym_client = APIClient()
#         self.anonym_client_with_cart = APIClient()
#         self.user_v_client = APIClient()
#         self.user_v_client.force_authenticate(
#             PaymentViewsTests.user_vendor)
#         self.user_client = APIClient()
#         self.user_authorized_client = APIClient()
#         self.user_authorized_client.force_authenticate(
#             PaymentViewsTests.user)
#         self.client_without_cart = APIClient()
#         self.client_without_cart.force_authenticate(
#             PaymentViewsTests.user_without_cart
#         )

#     def test_user_v_get_status(self):
#         """Получение статуса заказа в Yookassa"""
#         order = Order.objects.get(id=2)
#         self.assertIsInstance(order, Order)
#         self.assertEqual(order.value, 900, 'ошибка суммы')
#         pay = OrderPayment.objects.get(value=900)
#         self.assertIsInstance(pay, OrderPayment)
#         payment_id = '2cdedfd4-000f-5000-8000-1be0be5d3862'
#         payment = Payment.find_one(payment_id)
#         pay.status = payment.status
#         pay.save(update_fields=('status',))
#         self.assertEqual(
#             pay.status, 'succeeded',
#             'Не удалось получить статус платежа'
#             f' {payment_id}'
#         )

#     def test_user_repeat_pay(self):
#         """Нельзя оплатить повторно оплаченный заказа в Yookassa"""
#         client = self.user_authorized_client
#         order = PaymentViewsTests.order_user
#         payment = PaymentViewsTests.payment_u
#         resp = client.get(f'/api/order/{order.id}/payment/{payment.id}/')
#         self.assertEquals(resp.status_code, HTTPStatus.OK)
#         self.assertEqual(resp.data.get('status'), 'succeeded')
#         resp = client.post(f'/api/order/{order.id}/payment/')
#         self.assertEquals(
#             resp.status_code, HTTPStatus.BAD_REQUEST,
#             'Платеж оплачен, нельзя оплатить повторно'
#         )

#     def test_user_pay_order(self):
#         """Проверка значений полей post-запрос"""
#         client = self.user_authorized_client
#         data_order = {
#             'user': 1,
#             'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
#             'phone': '+79991243584',
#             'comment': 'Срочно',
#         }
#         response = client.post('/api/order/', data=data_order)
#         self.assertEquals(response.status_code, HTTPStatus.CREATED)
#         order_id = response.data.get('id')
#         resp = client.post(f'/api/order/{order_id}/payment/')
#         ui = (r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[45][0-9a-f]{3}'
#               r'-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}$')
#         expected_data = {
#             'idempotence_key': ui,
#             'order': 3,
#             'payment_id': ui,
#             'status': 'pending',
#             'is_paid': False,
#             'confirmation_url': (
#                 'https://yoomoney.ru/checkout/payments/v2/contract?orderId'
#             ),
#             'value': '1728.00'
#         }
#         self.assertEquals(resp.status_code, HTTPStatus.CREATED)
#         self.check_fields(resp.data, expected_data)
#         resp_1 = client.post(f'/api/order/{order_id}/payment/')
#         self.assertEquals(resp_1.status_code, HTTPStatus.CREATED)
#         self.assertEqual(
#             resp.data.get('id'), resp_1.data.get('id'),
#             'Не создавать платеж, предыдущий не отменен'
#         )
#         payment = OrderPayment.objects.get(order=order_id)
#         payment.status = 'canceled'
#         payment.save()
#         resp_2 = client.post(f'/api/order/{order_id}/payment/')
#         self.assertEquals(resp_2.status_code, HTTPStatus.CREATED)
#         self.assertNotEqual(
#             resp.data.get('id'), resp_2.data.get('id'),
#             'Необходимо создать платеж, после отмены предыдущего'
#         )
#         re_get = client.get(f'/api/order/{order_id}/payment/')
#         self.assertEquals(re_get.status_code, HTTPStatus.OK)
#         self.assertEqual(2, len(re_get.data))

#     def check_fields(self, response, expected_data):
#         if type(expected_data) is list and expected_data:
#             for i in range(len(expected_data)):
#                 self.check_fields(
#                     response=response[i], expected_data=expected_data[i])
#         elif type(expected_data) is str:
#             with self.subTest():
#                 self.assertEqual(
#                     response,
#                     expected_data,
#                 )
#         else:
#             for key, expected_value in expected_data.items():
#                 if type(expected_value) is list and expected_value:
#                     for j in range(len(expected_value)):
#                         self.check_fields(response=response.get(
#                             key)[j], expected_data=expected_value[j])
#                 else:
#                     if type(expected_value) is dict and expected_value:
#                         self.check_fields(response=response.get(
#                             key), expected_data=expected_value)
#                     else:
#                         with self.subTest(key=key):
#                             if key == 'confirmation_url':
#                                 self.assertEqual(
#                                     response.get(key).split('=')[0],
#                                     expected_value,
#                                     f'{key}'
#                                 )
#                             elif key in [
#                                 'idempotence_key', 'payment_id',
#                             ]:
#                                 self.assertIsNotNone(
#                                     re.match(expected_value,
#                                              response.get(key)),
#                                     f'{key}'
#                                 )
#                             else:
#                                 self.assertEqual(
#                                     response.get(key),
#                                     expected_value,
#                                     f'{key}'
#                                 )

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
#         super().tearDownClass()


# @override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
# class RepaymentViewsTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.small_gif = (
#             b'\x47\x49\x46\x38\x39\x61\x02\x00'
#             b'\x01\x00\x80\x00\x00\x00\x00\x00'
#             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
#             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
#             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
#             b'\x0A\x00\x3B'
#         )
#         cls.product = Product.objects.create(
#             name='Овощерезка1',
#             description='Хороший продукт',
#             price=180,
#             code=1691105841,
#             vendor_code='артикул овощерезки',
#             is_deleted=False,
#         )
#         cls.product_grater = Product.objects.create(
#             name='Терка1',
#             description='Хороший продукт',
#             price=18,
#             code=1691109841,
#             vendor_code='артикул терки',
#             is_deleted=False,
#         )
#         cls.uploaded = SimpleUploadedFile(
#             name='prod_img.gif',
#             content=cls.small_gif,
#             content_type='image/gif'
#         )
#         cls.image = ProductImage.objects.create(
#             product=cls.product,
#             image=cls.uploaded
#         )
#         cls.admin = User.objects.create_superuser(
#             'test_user3@example.com', 'test_pass')
#         cls.user = User.objects.create_user(
#             'test_user4@example.com', 'test_pass')
#         cls.order = Order.objects.create(
#             user=cls.user,
#             phone='+79991243584',
#             email=cls.user.email,
#             address='г.Москва, ул. Ленина, д. 41, к. 2'
#         )
#         cls.order = Order.objects.create(
#             user=cls.user,
#             phone='+79991243584',
#             email=cls.user.email,
#             address='г.Москва, ул. Ленина, д. 41, к. 2'
#         )
#         cls.order = Order.objects.create(
#             user=cls.user,
#             phone='+79991243584',
#             email=cls.user.email,
#             address='г.Москва, ул. Ленина, д. 41, к. 2'
#         )
#         cls.commodity = Commodity.objects.create(
#             product=cls.product,
#             quantity=10,
#             order=cls.order
#         )
#         cls.commodity1 = Commodity.objects.create(
#             product=cls.product_grater,
#             quantity=10,
#             order=cls.order
#         )
#         cls.payment = OrderPayment.objects.create(
#             idempotence_key='1032104c-9836-4307-a726-4ea0b76e9b54',
#             order=cls.order,
#             payment_id='2cef02a5-000f-5000-9000-1074b91d9c44',
#         )
#         cls.order_refunds = OrderRefund.objects.create(
#             order=cls.order
#         )
#         cls.commodity_ref = CommodityRefund.objects.create(
#             refund=cls.order_refunds,
#             commodity=cls.commodity,
#             quantity=10,
#         )
#         cls.commodity_ref1 = CommodityRefund.objects.create(
#             refund=cls.order_refunds,
#             commodity=cls.commodity1,
#             quantity=10,
#         )
#         cls.repayment = Repayment.objects.create(
#             idempotence_key='edfef270-befa-48b8-b224-8ca5476fe8a1',
#             refund_id='2cef0fb2-0015-5000-9000-1b8f2d97d600',
#             payment=cls.payment,
#             order_refund=cls.order_refunds
#         )

#     def setUp(self):
#         self.user_authorized_client = APIClient()
#         self.user_authorized_client.force_authenticate(
#             RepaymentViewsTests.user)
#         self.admin_client = APIClient()
#         self.admin_client.force_authenticate(
#             RepaymentViewsTests.admin
#         )

#     def test_create_repayment(self):
#         """Создание возврата администратором"""
#         user_client = self.user_authorized_client
#         url = '/api/cart/'
#         cart = {
#             'product': 1,
#             'amount': 1
#         }
#         resp = user_client.post(url, cart)
#         self.assertEquals(
#             resp.status_code, HTTPStatus.CREATED,
#             'Не создана корзина с товаром'
#         )
#         resp = user_client.post('/api/order/')
#         self.assertEquals(
#             resp.status_code, HTTPStatus.CREATED,
#             'Не создана заказ с товаром'
#         )
#         order_id = resp.data.get('id')
#         resp = user_client.post(f'/api/order/{order_id}/payment/')
#         print(resp.json())
#         self.assertEquals(
#             resp.status_code, HTTPStatus.CREATED,
#             'Не создан платеж'
#         )
#         resp = user_client.post(f'/api/order/{order_id}/cancel/')
#         print(resp.status_code)
#         print(resp.json())
#         resp = user_client.get(f'/api/order/{order_id}/refund/')
#         self.assertEquals(
#             resp.status_code, HTTPStatus.OK,
#             'Нет возврата заказа'
#         )
#         refund = resp.data[0].get('id')
#         resp = self.admin_client.post(
#             f'/api/order/{order_id}/refund/{refund}/repayment/')
#         print(resp.status_code)
#         print(resp.json())
#         self.assertEquals(
#             resp.status_code, HTTPStatus.CREATED,
#             'Возврат платежа не выполнен'
#         )
#         resp = self.admin_client.get(
#             f'/api/order/{order_id}/refund/{refund}/repayment/')
#         print(resp.status_code)
#         print(resp.json())
#         Repayment.objects.all()
#         self.assertEquals(
#             resp.status_code, HTTPStatus.OK,
#             'Нет возврата заказа'
#         )
#         print(resp.json())
#         pass

#     def test_create_repayment1(self):
#         """Создание возврата администратором"""
#         """Для успешного прохождения теста .env должен содержать
#         : Y_SECRET_KEY=*** Y_SHOP_ID=***.
#         Тест выполняется вручную, т.к. необходимо выполнить
#         подтверждение оплаты на стороне yookassa
#         """
#         order = RepaymentViewsTests.order
#         user_client = self.user_authorized_client
#         resp = user_client.get(f'/api/order/{order.id}/payment/1/')
#         self.assertEquals(
#             resp.status_code, HTTPStatus.OK,
#             'Нет платежа'
#         )
#         print(resp.json())
#         print(Payment.find_one('2cef02a5-000f-5000-9000-1074b91d9c44').status)
#         url = f'/api/order/{order.id}/refund/1/'
#         resp = user_client.get(url)
#         self.assertEquals(
#             resp.status_code, HTTPStatus.OK,
#             'Не оформлен возврат заказа'
#         )
#         print(resp.json())
#         url = f'/api/order/{order.id}/refund/1/repayment/'
#         resp = user_client.post(url)
#         self.assertEquals(
#             resp.status_code, HTTPStatus.FORBIDDEN,
#             'Пользователь не может провести возврат платежа'
#         )
#         admin_client = self.admin_client
#         url = f'/api/order/{order.id}/refund/1/repayment/'
#         resp = admin_client.post(url)
#         self.assertEquals(
#             resp.status_code, HTTPStatus.CREATED,
#             'Не произведен возврат платежа'
#         )
#         url = f'/api/order/{order.id}/refund/1/repayment/'
#         resp = admin_client.post(url)
#         self.assertEquals(
#             resp.status_code, HTTPStatus.BAD_REQUEST,
#             'Нельзя повторно провести возврат платежа'
#         )
#         print(resp.json())
#         url = f'/api/order/{order.id}/refund/1/repayment/1/'
#         resp = admin_client.get(url)
#         self.assertEquals(
#             resp.status_code, HTTPStatus.OK,
#             'Не получены данные по возврату платежа'
#         )
#         print(resp.json())

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
#         super().tearDownClass()
