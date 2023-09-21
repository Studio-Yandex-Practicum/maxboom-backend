from django.test import TestCase, override_settings
from catalogue.models import (
    Category, Product, Brand,
    ProductImage, CategoryTree
)
import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class BrandModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = Brand.objects.create(
            name='Бренд',
            slug='brand',
        )

    def test_models_have_correct_object_name(self):
        brand = BrandModelTest.brand
        expected_brand_name = brand.name
        self.assertEqual(
            expected_brand_name, str(brand)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        brand = BrandModelTest.brand
        field_verboses = {
            'name': 'Наименование',
            'slug': 'Уникальный слаг',
            'is_prohibited': 'Запрещенный для публикации производитель',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    brand._meta.get_field(field).verbose_name, expected_value,
                    f'Ошибка в поле {field} '
                )

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


class CategoryTreeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_root = Category.objects.create(
            name='Категория2',
        )
        cls.category_affiliated = Category.objects.create(
            name='Категория3',
        )
        cls.category_tree = CategoryTree.objects.create(
            root=CategoryTreeModelTest.category_root,
            branch=CategoryTreeModelTest.category_affiliated
        )

    def test_models_have_correct_object_name(self):
        category_root = CategoryTreeModelTest.category_root
        category_affiliated = CategoryTreeModelTest.category_affiliated
        category_tree = CategoryTreeModelTest.category_tree
        expected = f'{category_root.name} {category_affiliated.name}'
        self.assertEqual(
            expected, str(category_tree)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        category_tree = CategoryTreeModelTest.category_tree
        field_verboses = {
            'root': 'Родительская категория',
            'branch': 'Дочерняя категория',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    category_tree._meta.get_field(field).verbose_name,
                    expected_value,
                    f'Ошибка в поле {field} '
                )

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


class CategoryModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Категория1',
            slug='category1',
            meta_title='мета-название',
            meta_description='мета-писание',
        )

    def test_models_have_correct_object_name(self):
        category = CategoryModelTest.category
        expected_category_name = category.name
        self.assertEqual(
            expected_category_name, str(category)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        category = CategoryModelTest.category
        field_verboses = {
            'name': 'Название',
            'slug': 'Уникальный слаг',
            'meta_title': 'Мета-название категории',
            'meta_description': 'Мета-описание категории',
            'is_visible_on_main': 'Категория видимая на главной странице',
            'is_prohibited': 'Запрещенная для публикации категория',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    category._meta.get_field(field).verbose_name,
                    expected_value,
                    f'Ошибка в поле {field} '
                )

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


class ProductModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = Product.objects.create(
            name='Автомобильный переходник ',
            description='Хороший продукт',
            price=180,
            code=168978277,
            wb_urls='https://www.wildberries.ru/catalog/168978277/detail.aspx'
        )

    def test_models_have_correct_object_name(self):
        product = ProductModelTest.product
        expected_product_name = product.name
        self.assertEqual(
            expected_product_name, str(product)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        product = ProductModelTest.product
        field_verboses = {
            'name': 'Название',
            'slug': 'Уникальный слаг',
            'description': 'Описание',
            'price': 'Цена',
            'brand': 'Бренд',
            'category': 'Категория',
            'code': 'Код товара',
            'wb_urls': 'Ссылка на WB',
            'quantity': 'Количество',
            'is_deleted': 'Удален ли товар',
            'meta_title': 'Мета-название товара',
            'meta_description': 'Мета-описание товара',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    product._meta.get_field(field).verbose_name, expected_value
                )

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProductImageModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = Product.objects.create(
            name='Автомобильный переходник1 ',
            description='Хороший продукт',
            price=180,
            code=1689782771,
            wb_urls='https://www.wildberries.ru/catalog/168978277/detail.aspx'
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.image = ProductImage.objects.create(
            product=ProductImageModelTest.product,
            image=uploaded
        )

    def test_models_have_correct_object_name(self):
        image = ProductImageModelTest.image
        expected_str = 'products_images/small.gif'
        self.assertEqual(
            expected_str, str(image)
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        image = ProductImageModelTest.image
        field_verboses = {
            'image': 'Изображение',
            'product': 'Продукт',
            'thumbnail': 'Эскиз'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    image._meta.get_field(field).verbose_name, expected_value,
                    f'Ошибка в поле {field} '
                )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().setUpClass()
