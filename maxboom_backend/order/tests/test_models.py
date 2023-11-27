import shutil
import tempfile
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from catalogue.models import Product
from order.models import Commodity, CommodityRefund, Order, OrderRefund

# from accounts.models import UserManager

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email='tt@tt.tt',
            password='12345'
        )
        cls.order = Order.objects.create(
            user=cls.user,
            phone='+79991243636',
            email=cls.user.email,
            address='г.Москва, ул. Ленина, д. 41, к. 2'
        )
        cls.product = Product.objects.create(
            name='Нож',
            description='Хороший продукт',
            price=180,
            code=1023236,
            vendor_code='артикул 1',
            wb_urls='https://www.wildberries.ru/catalog/1023236/detail.aspx',
            is_deleted=False,
        )
        cls.commodity = Commodity.objects.create(
            product=cls.product,
            quantity=2,
            order=cls.order
        )
        cls.order_new = Order.objects.create(
            user=cls.user,
            phone='+79991243686',
            email=cls.user.email,
            address='г.Москва, ул. Ленина, д. 41, к. 3'
        )
        cls.product_new = Product.objects.create(
            name='Нож новый',
            description='Хороший продукт',
            price=100,
            code=1023237,
            vendor_code='артикул 2',
            wb_urls='https://www.wildberries.ru/catalog/1023237/detail.aspx',
            is_deleted=False,
        )
        cls.commodity_new = Commodity.objects.create(
            price=cls.product_new.price,
            product=cls.product_new,
            quantity=3,
            order=cls.order_new,
        )

    def test_create_model(self):
        """корректное значение полей созданной модели"""
        user = OrderModelTest.user
        self.assertTrue(
            Order.objects.filter(user=user).exists(),
            f'Не создана модель привязанная к {user}'
        )
        order = Order.objects.get(user=user, id=1)
        expected_data = {
            'user': user,
            'phone': '+79991243636',
            'email': user.email,
            'address': 'г.Москва, ул. Ленина, д. 41, к. 2',
        }
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(order, field), expected_value,
                    f'Ошибка в поле {field} '
                )

    def test_models_have_correct_object_name(self):
        """корректное строчное представление объекта модели"""
        order = OrderModelTest.order
        expected_product_name = f'Заказ № {order.id}.'
        self.assertEqual(
            expected_product_name, str(order)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        order = OrderModelTest.order
        field_verboses = {
            'user': 'Пользователь',
            'is_active': 'Авторизованный',
            'session_id': 'id сессии',
            'address': 'Адрес',
            'phone': 'Телефон',
            'email': 'Почта',
            'comment': 'Комментарии',
            'created': 'Дата создания',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    order._meta.get_field(field).verbose_name, expected_value
                )

    def test_value_property(self):
        """корректный расчет стоимости"""
        order = OrderModelTest.order
        self.assertEqual(
            order.value, 288,
            'Неверный расчет стоимости заказа'
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderRefundModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email='ttеs@tta.tt',
            password='12345866'
        )
        cls.order = Order.objects.create(
            user=cls.user
        )
        cls.product = Product.objects.create(
            name='Хлебница',
            description='',
            price=185,
            code=1023283,
            vendor_code='артикул Хлебницы',
            wb_urls='https://www.wildberries.ru/catalog/1023283/detail.aspx',
            is_deleted=False,
        )
        cls.commodity = Commodity.objects.create(
            product=cls.product,
            quantity=10,
            order=cls.order
        )
        cls.session_id = uuid.uuid4()
        cls.order = Order.objects.create(
            user=cls.user,
            phone='+79991243686',
            email=cls.user.email,
            address='г.Москва, ул. Ленина, д. 41, к. 3'
        )
        cls.order_refund = OrderRefund.objects.create(
            order=cls.order
        )
        cls.commodity_refund = CommodityRefund.objects.create(
            refund=cls.order_refund,
            quantity=1,
            commodity=cls.commodity
        )

    def test_commodity_refund(self):
        """корректное значение полей модели возврата заказа"""
        order_refund = OrderRefundModelTest.order_refund
        commodity = OrderRefundModelTest.commodity
        commodity_refund = CommodityRefund.objects.filter(
            refund=order_refund,
            commodity=commodity
        )
        self.assertTrue(commodity_refund.exists(),
                        'нет возвращаемого товара')
        commodity_refund = CommodityRefund.objects.get(
            refund=order_refund,
            commodity=commodity
        )
        expected_data = {
            'refund': order_refund,
            'quantity': 1,
            'commodity': commodity
        }
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(commodity_refund, field), expected_value,
                    f'Ошибка в поле {field} '
                )

    def test_commodity_refund_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        commodity_refund = OrderRefundModelTest.commodity_refund
        field_verboses = {
            'commodity': 'Возвращаемый товар',
            'refund': 'Возврат',
            'quantity': 'Количество'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    commodity_refund._meta.get_field(
                        field).verbose_name, expected_value
                )

    def test_order_refund(self):
        """корректное значение полей модели возврата заказа"""
        order = OrderRefundModelTest.order
        order_refund = OrderRefund.objects.filter(order=order)
        self.assertTrue(order_refund.exists(), 'нет возврата заказа')
        order_refund = OrderRefund.objects.get(order=order)
        expected_data = {
            'order': order
        }
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(order_refund, field), expected_value,
                    f'Ошибка в поле {field} '
                )

    def test_order_refund_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        order_refund = OrderRefundModelTest.order_refund
        field_verboses = {
            'order': 'Заказ'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    order_refund._meta.get_field(
                        field).verbose_name, expected_value
                )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CommodityModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email='ttе@tta.tt',
            password='12345866'
        )
        cls.order = Order.objects.create(
            user=cls.user
        )
        cls.product = Product.objects.create(
            name='Вилка',
            description='Хороший продукт',
            price=180,
            code=102328,
            vendor_code='артикул 1',
            wb_urls='https://www.wildberries.ru/catalog/102328/detail.aspx',
            is_deleted=False,
        )
        cls.commodity = Commodity.objects.create(
            product=cls.product,
            quantity=1,
            order=cls.order
        )
        cls.session_id = uuid.uuid4()
        cls.order_session = Order.objects.create(
            email='test@ee.ee',
            session_id=cls.session_id,
            is_active=False
        )
        cls.commodity_anonym = Commodity.objects.create(
            order=cls.order_session,
            product=cls.product,
            quantity=3
        )

    def test_anonym_commodity(self):
        """корректное значение полей модели анонимного пользователя"""
        order = CommodityModelTest.order_session
        commodity = order.commodities.all()[0]
        self.assertFalse(order.is_active)
        self.assertEqual(order.value, 432)
        expected_data = {
            'price': 144,
            'product': CommodityModelTest.product,
            'quantity': 3,
            'order': order
        }
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(commodity, field), expected_value,
                    f'Ошибка в поле {field} '
                )

    def test_immutable_price(self):
        """неизменная цена в заказе, при изменении цены товара"""
        product_add = Product.objects.create(
            name='Чайная ложка',
            description='Хороший продукт',
            price=150,
            code=102333,
            vendor_code='артикул 2',
            wb_urls='https://www.wildberries.ru/catalog/102333/detail.aspx',
            is_deleted=False,
        )
        order = CommodityModelTest.order
        commodity_add = Commodity.objects.create(
            product=product_add, order=order, quantity=2
        )
        price_old = order.commodities.get(product=product_add)
        product_add.price = 200
        product_add.save()
        commodity_add.quantity = 3
        commodity_add.save()
        price_new = order.commodities.get(product=product_add)
        self.assertEqual(price_new, price_old)
        self.assertEqual(3, commodity_add.quantity)
        self.assertNotEqual(commodity_add.product.price, 150)

    def test_create_model(self):
        """корректное значение полей созданной модели"""
        product = CommodityModelTest.product
        self.assertTrue(
            Commodity.objects.filter(product=product).exists(),
            f'Не создана модель привязанная к {product}'
        )
        commodity = Commodity.objects.get(
            product=product,
            order=CommodityModelTest.order
        )
        expected_data = {
            'price': 144,
            'product': product,
            'quantity': 1,
            'order': CommodityModelTest.order

        }
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(commodity, field), expected_value,
                    f'Ошибка в поле {field} '
                )

    def test_models_have_correct_object_name(self):
        """корректное строчное представление объекта модели"""
        product = CommodityModelTest.product
        commodity = CommodityModelTest.commodity
        expected_product_name = product.name
        self.assertEqual(
            expected_product_name, str(commodity)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        commodity = CommodityModelTest.commodity
        field_verboses = {
            'product': 'Товар в заказе',
            'quantity': 'Количество',
            'price': 'Цена',
            'order': 'Заказ'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    commodity._meta.get_field(
                        field).verbose_name, expected_value
                )

    def test_get_rest(self):
        """получение остатка товара в заказе после возвратов"""
        commodity = CommodityModelTest.commodity
        self.assertEqual(
            commodity.rest, 1,
            'Ошибка расчета остатка товара в заказе'
        )
        order = CommodityModelTest.order
        order_refund = OrderRefund.objects.create(
            order=order
        )
        CommodityRefund.objects.create(
            refund=order_refund, commodity=commodity,
            quantity=1
        )
        self.assertEqual(
            commodity.rest, 0,
            'Ошибка расчета остатка товара в заказе'
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
