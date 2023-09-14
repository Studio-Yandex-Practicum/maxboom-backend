# import shutil
# import tempfile
# from typing import OrderedDict

# from django.test import override_settings, TestCase
# from django.contrib.auth import get_user_model
# from django.core.files.uploadedfile import SimpleUploadedFile
# from rest_framework import status

# from blog.models import Post, Category, PostTag, Tag


# MEDIA_ROOT = tempfile.mkdtemp()

# User = get_user_model()


# @override_settings(MEDIA_ROOT=MEDIA_ROOT)
# class NewsViewTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         """
#         Создание поста, категории, тега и админа
#         для всего тестирования.
#         """
#         print('START!!!')
#         super().setUpClass()
#         cls.admin = User.objects.create_superuser(
#             'admin@admin.com', 'admin')
#         cls.category = Category.objects.create(
#             title='Тестовая категория',
#             slug='test-category')
#         cls.tag = Tag.objects.create(
#             name='Тестовый тег')
#         cls.post = Post.objects.create(
#             title='Тестовый пост',
#             text='Текст для тестов',
#             author=User.objects.filter(
#                 email='admin@admin.com')[0],
#             image=SimpleUploadedFile(
#                 'test.jpg', b'something'),
#             category=Category.objects.filter(
#                 title='Тестовая категория')[0],
#             slug='test-slug')
#         cls.post.tags.set([cls.tag])

#     @classmethod
#     def tearDownClass(cls):
#         """
#         Удаление временной папки для медиа после всех тестов.
#         """
#         shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
#         super().tearDownClass()

#     def test_posts_list_unauthenticated(self):
#         """
#         Получение списка всех постов
#         для неавторизованных пользователей.
#         """
#         print('BEGIN!')
#         response = self.client.get(
#             '/api/shopblog/posts/')
#         instance = Post.objects.first()
#         # print(f'instance {instance}')
#         # print(
#         #     f'post.objects.filter {Post.objects.filter(slug="test-slug")}')
#         # queryset = Post.objects.filter(slug='test-slug')
#         # instance = queryset[0]
#         url_image = 'http://testserver/media/' + str(instance.image)
#         pub_date = instance.pub_date.strftime('%Y-%m-%d')
#         print(f' instance.category = {instance.category}')
#         expected_data = {
#             'id': instance.pk,
#             'title': instance.title,
#             'text': instance.text,
#             'image': url_image,
#             'pub_date': pub_date,
#             'author': 'Администратор',
#             'category': instance.category,
#             'tags': instance.tags,
#             'slug': instance.slug
#         }
#         for key, expected_value in expected_data.items():
#             with self.subTest(key=key):
#                 # print(response.data.get('results')[0].get(key))
#                 if key != 'category' and key != 'tags':
#                     self.assertEqual(
#                         response.data.get('results')[0].get(key),
#                         expected_value)
#                 elif key == 'category':
                    
#         # print(f'response.data {response.data.get("results")[0].get("category")}')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
