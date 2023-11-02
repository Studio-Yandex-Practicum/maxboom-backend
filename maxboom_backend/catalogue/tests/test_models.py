import os
import shutil
import tempfile

from catalogue.models import Brand, Category, Product, ProductImage
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from pytils.translit import slugify

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class BrandModelTest(TestCase):
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
            is_prohibited=True,
            is_visible_on_main=True,
            image=cls.uploaded
        )

    def test_create_model(self):
        '''корректное значение полей созданной модели'''
        expected_data = {
            'name': 'Бренд',
            'is_prohibited': True,
            'is_visible_on_main': True,
        }
        brand = BrandModelTest.brand
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(brand, field), expected_value,
                    f'Ошибка в поле {field} '
                )
        self.assertEqual(
            brand.image.name,
            f'brand-images/{brand.slug}/{BrandModelTest.uploaded.name}'
        )

    def test_delete_image_file(self):
        uploaded = SimpleUploadedFile(
            name='logo_brand_test.gif',
            content=BrandModelTest.small_gif,
            content_type='image/gif'
        )
        brand = Brand.objects.create(
            name='Бренд тест',
            image=uploaded
        )
        image_exists = brand.image.path
        self.assertTrue(
            os.path.exists(
                image_exists), 'Не существует файла изображения до удаления'
        )
        brand.delete()
        self.assertFalse(
            os.path.exists(image_exists), 'Старый файл изображения не удален'
        )

    def test_update_image_file(self):
        '''удаление файла изображения при обновлении объекта модели'''
        brand_item = BrandModelTest.brand
        small_new_gif = BrandModelTest.small_gif
        new_image = SimpleUploadedFile(
            name='logo_new.gif',
            content=small_new_gif,
            content_type='image/gif'
        )
        image_exists = brand_item.image.path

        self.assertTrue(
            os.path.exists(
                image_exists), 'Не существует файла изображения до обновления'
        )
        brand_item.image = new_image
        brand_item.save()
        image_new = brand_item.image.path
        self.assertTrue(
            os.path.exists(image_new),
            'Не существует нового файла изображения после обновления'
        )
        self.assertFalse(
            os.path.exists(image_exists), 'Старый файл изображения не удален'
        )

    def test_add_slug(self):
        '''корректное добавление slug'''
        brand = Brand.objects.create(
            name='МаксБум',
        )
        self.assertEqual(
            brand.slug, slugify(brand.name)[:200]
        )

    def test_models_have_correct_object_name(self):
        '''корректное строчное представление объекта модели'''
        brand = BrandModelTest.brand
        expected_brand_name = brand.name
        self.assertEqual(
            expected_brand_name, str(brand)
        )

    def test_verbose_name(self):
        '''verbose_name в полях совпадает с ожидаемым'''
        brand = BrandModelTest.brand
        field_verboses = {
            'name': 'Наименование',
            'slug': 'Уникальный слаг',
            'is_prohibited': 'Запрещенный для публикации производитель',
            'is_visible_on_main': 'Производитель на главной странице',
            'image': 'Логотип'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    brand._meta.get_field(field).verbose_name, expected_value,
                    f'Ошибка в поле {field} '
                )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


class CategoryModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_root = Category.objects.create(
            name='Категория тестовая',
            wb_category_id=12345
        )
        cls.category = Category.objects.create(
            name='Категория1',
            is_visible_on_main=True,
            is_prohibited=True,
            root=cls.category_root,
            wb_category_id=12346
        )

    def test_add_slug(self):
        '''корректное значение slug'''
        category = CategoryModelTest.category
        category_new = Category.objects.create(
            name='Категория2',
            root=category,
            wb_category_id=12347
        )
        self.assertEqual(
            category_new.slug, slugify(category_new.name)[:200]
        )

    def test_create_model(self):
        '''корректное значение полей созданной модели'''
        self.assertTrue(Category.objects.filter(name='Категория1').exists())
        category = Category.objects.get(name='Категория1')

        expected_data = {
            'name': 'Категория1',
            'is_visible_on_main': True,
            'is_prohibited': True,
            'root': CategoryModelTest.category_root,
        }
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(category, field), expected_value,
                    f'Ошибка в поле {field} '
                )

    def test_models_have_correct_object_name(self):
        '''корректное строчное представление объекта модели'''
        category = CategoryModelTest.category
        expected_category_name = category.name
        self.assertEqual(
            expected_category_name, str(category)
        )

    def test_verbose_name(self):
        '''verbose_name в полях совпадает с ожидаемым.'''
        category = CategoryModelTest.category
        field_verboses = {
            'name': 'Название',
            'slug': 'Уникальный слаг',
            'is_visible_on_main': 'Категория видимая на главной странице',
            'is_prohibited': 'Запрещенная для публикации категория',
            'root': 'Родительская категория'
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
        super().tearDownClass()


class ProductModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = Brand.objects.create(
            name='Бренд',
            slug='brand',
        )
        cls.category = Category.objects.create(
            name='Категория1',
            slug='category1',
            wb_category_id=12348
        )
        cls.product = Product.objects.create(
            name='Пусковое зарядное устройство 2',
            description='Хороший продукт для',
            price=180,
            brand=cls.brand,
            category=cls.category,
            code=169110394,
            vendor_code='артикул 1',
            wb_urls='https://www.wildberries.ru/catalog/169110394/detail.aspx',
            is_deleted=True,
        )

    def test_create_model(self):
        '''корректное значение полей созданной модели'''
        self.assertTrue(Product.objects.filter(
            name='Пусковое зарядное устройство 2').exists())
        product = Product.objects.get(name='Пусковое зарядное устройство 2')
        expected_data = {
            'name': 'Пусковое зарядное устройство 2',
            'description': 'Хороший продукт для',
            'price': 180,
            'brand': ProductModelTest.brand,
            'category': ProductModelTest.category,
            'code': 169110394,
            'wb_urls': ('https://www.wildberries.ru/'
                        'catalog/169110394/detail.aspx'),
            'is_deleted': True,
        }
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(product, field), expected_value,
                    f'Ошибка в поле {field} '
                )

    def test_add_slug(self):
        '''корректное добавление slug'''
        product = Product.objects.create(
            name='Пусковое зарядное устройство ',
            description='Хороший продукт для',
            price=180,
            code=1691103945,
            vendor_code='артикул 2',
            wb_urls='https://www.wildberries.ru/catalog/1691103945/detail.aspx'
        )
        self.assertEqual(
            product.slug,
            f'{slugify(product.name)}-{slugify(product.code)}'
        )

    def test_models_have_correct_object_name(self):
        '''корректное строчное представление объекта модели'''
        product = ProductModelTest.product
        expected_product_name = product.name
        self.assertEqual(
            expected_product_name, str(product)
        )

    def test_verbose_name(self):
        '''verbose_name в полях совпадает с ожидаемым.'''
        product = ProductModelTest.product
        field_verboses = {
            'name': 'Название',
            'slug': 'Уникальный слаг',
            'description': 'Описание',
            'price': 'Цена',
            'brand': 'Производитель',
            'category': 'Категория',
            'code': 'Код товара',
            'wb_urls': 'Ссылка на WB',
            'quantity': 'Количество',
            'is_deleted': 'Удаленный товар',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    product._meta.get_field(field).verbose_name, expected_value
                )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


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
            wb_urls='https://www.wildberries.ru/catalog/168978277/detail.aspx',
            vendor_code='артикул 3'
        )
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.image = ProductImage.objects.create(
            product=cls.product,
            image=cls.uploaded
        )

    def test_create_model(self):
        prod_pk = ProductImageModelTest.product.pk
        self.assertTrue(ProductImage.objects.filter(product=prod_pk).exists())
        image = ProductImage.objects.get(product=prod_pk)
        expected_data = {
            'product': ProductImageModelTest.product,
        }
        for field, expected_value in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(image, field), expected_value,
                    f'Ошибка в поле {field} '
                )
        self.assertEqual(
            image.image.name,
            f'product-images/{image.product.slug}/'
            f'{ProductImageModelTest.uploaded.name}'
        )

    def test_update_image_file(self):
        '''удаление файла изображения при обновлении объекта модели'''
        prod_image_item = ProductImageModelTest.image
        new_image = SimpleUploadedFile(
            name='small_new.gif',
            content=ProductImageModelTest.small_gif,
            content_type='image/gif'
        )
        image_exists = prod_image_item.image.path

        self.assertTrue(
            os.path.exists(
                image_exists), 'Не существует файла изображения до обновления'
        )
        prod_image_item.image = new_image
        prod_image_item.save()
        image_new = prod_image_item.image.path
        self.assertTrue(
            os.path.exists(image_new),
            'Не существует нового файла изображения после обновления'
        )
        self.assertFalse(
            os.path.exists(image_exists), 'Старый файл изображения не удален'
        )

    def test_delete_image_file_(self):
        '''удаление файла изображения при удалении объекта модели'''
        product = Product.objects.create(
            name='Автомобильный переходник3 ',
            description='Хороший продукт',
            price=180,
            code=16897827713,
            vendor_code='артикул 4',
            wb_urls=('https://www.wildberries.ru/catalog/'
                     '16897827713/detail.aspx')
        )
        small_add = SimpleUploadedFile(
            name='small_add.gif',
            content=ProductImageModelTest.small_gif,
            content_type='image/gif'
        )
        prod_image_item = ProductImage.objects.create(
            product=product,
            image=small_add
        )
        image_exists = prod_image_item.image.path
        self.assertTrue(
            os.path.exists(
                image_exists), 'Не существует файла изображения до удаления'
        )
        prod_image_item.delete()
        self.assertFalse(
            os.path.exists(image_exists), 'Старый файл изображения не удален'
        )

    def test_models_have_correct_object_name(self):
        '''корректное строчное представление объекта модели'''
        image = ProductImageModelTest.image
        expected_str = f'product-images/{image.product.slug}/small.gif'
        self.assertEqual(
            expected_str, str(image)
        )

    def test_verbose_name(self):
        '''verbose_name в полях совпадает с ожидаемым'''
        image = ProductImageModelTest.image
        field_verboses = {
            'image': 'Изображение',
            'product': 'Продукт',
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
        super().tearDownClass()
