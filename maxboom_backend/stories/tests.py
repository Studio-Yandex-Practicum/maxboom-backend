from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from stories.models import Story, Picture


User = get_user_model()


class StoriesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.story1 = Story.objects.create(
            name="Story 1",
            link="https://example.com/story1/",
            show=True
        )
        self.story2 = Story.objects.create(
            name="Story 2",
            link="https://example.com/story2/",
            show=True
        )

    def test_retrieve_stories(self):
        response = self.client.get('/api/stories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], 'Story 1')
        self.assertEqual(
            response.data['results'][0]['link'], 'https://example.com/story1/'
        )
        self.assertEqual(response.data['results'][1]['name'], 'Story 2')
        self.assertEqual(
            response.data['results'][1]['link'], 'https://example.com/story2/'
        )


class StoriesAdminCreationAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            email='admin_story@example.com', password='password'
        )
        self.client.login(email='admin_story@example.com', password='password')
        self.picture = Picture.objects.create(image='image.jpg')
        # self.client = APIClient()

    def test_create_story(self):
        data = {'name': 'New Story',
                'link': 'https://example.com/new-story/',
                'pictures': self.picture,
                'show': True}
        response = self.client.post(
            reverse('admin:stories_story_add'),
            data=data,
            # content_type='multipart/form-data',
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertTrue(Story.objects.filter(name='New Story').exists())


class StoriesAssociatedPituresAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.story = Story.objects.create(
            name="Story 1", link="https://example.com/story1/"
        )
        self.picture = Picture.objects.create(image='image.jpg')

    def test_associate_picture_with_story(self):
        data = {'pictures': [self.picture.id]}
        response = self.client.post(
            reverse('admin:stories_story_change', args=[self.story.id]),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.story.pictures.count(), 1)
