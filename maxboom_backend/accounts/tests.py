# flake8: noqa
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**self.user_data)
        self.assertEqual(admin_user.email, self.user_data['email'])
        self.assertTrue(admin_user.check_password(self.user_data['password']))
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_authentication(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('admin:login'), {
            'username': self.user_data['email'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_authentication(self):
        response = self.client.post(reverse('admin:login'), {
            'username': self.user_data['email'],
            'password': 'invalidpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'введите корректные Почта и пароль учётной записи'
        )

    def test_user_profile_creation(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertIsNotNone(user.userprofile)


class EmailVerificationTest(APITestCase):

    # endpoints needed
    register_url = "/api/users/"
    activate_url = "/api/users/activation/"
    login_url = "/api/token/login/"
    user_details_url = "/api/users/"
    resend_verification_url = "/api/users/resend_activation/"
    # user infofmation
    user_data = {
        "email": "test@example.com",
        "password": "verysecret"
    }
    login_data = {
        "email": "test@example.com",
        "password": "verysecret"
    }

    def test_register_with_email_verification(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be send
        self.assertEqual(len(mail.outbox), 1)

        # parse email to get uid and token
        email_lines = mail.outbox[0].body.splitlines()
        # you can print email to check it
        # print(mail.outbox[0].subject)
        # print(mail.outbox[0].body)
        activation_link = [l for l in email_lines if "/user-activation/" in l][0]

        uid, token = activation_link.split("/")[-2:]

        # verify email
        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # login to get the authentication token
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertTrue("auth_token" in response.json())
        token = response.json()["auth_token"]

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # get user details
        response = self.client.get(self.user_details_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["email"], self.user_data["email"])

    def test_register_resend_verification(self):

        response = self.client.post(self.register_url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(mail.outbox), 1)


        # clear the auth_token in header
        self.client.credentials()
        # resend the verification email
        data = {"email": self.user_data["email"]}
        response = self.client.post(self.resend_verification_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # there should be two emails in the outbox
        self.assertEqual(len(mail.outbox), 2)
        r = get_user_model().objects.last()
        self.assertFalse(r.is_active)

        # parse the last email
        email_lines = mail.outbox[1].body.splitlines()
        activation_link = [l for l in email_lines if "/user-activation/" in l][0]
        uid, token = activation_link.split("/")[-2:]

        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        r = get_user_model().objects.last()
        self.assertTrue(r.is_active)

        # login to get the authentication token
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertTrue("auth_token" in response.json())
        token = response.json()["auth_token"]

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # try to get user details
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
