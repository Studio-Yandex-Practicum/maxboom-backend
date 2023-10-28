# flake8: noqa
import tempfile
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from catalogue.models import Product, ProductImage
from cart.models import Cart, ProductCart


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CartTestCase(TestCase):

    image_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    image = SimpleUploadedFile(
        'image_gif.gif',
        image_gif,
        content_type='image/gif',
    )
    user_data = {
        'email': 'test_example@test',
        'password': 'testpassword1',
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

