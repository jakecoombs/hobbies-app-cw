import datetime
import os

from bs4 import BeautifulSoup

from .database import info
from django.test import TestCase
from django.contrib import auth
from django.urls import reverse_lazy

from .models import User

TEST_USERNAME = 'user'
TEST_USERNAME2 = "newuser"
TEST_PASSWORD = 'password123'
TEST_DOB = datetime.datetime.now()
TEST_EMAIL = "user@example.com"
CREDS = {
    "username": TEST_USERNAME,
    "password": TEST_PASSWORD,
    "dob": TEST_DOB,
    "email": TEST_EMAIL
}

# This basic tests is to be used as an example for running tests in S2I
# and OpenShift when building an application image.
class DbEngine(TestCase):
    def setUp(self):
        os.environ['ENGINE'] = 'SQLite'

    def test_engine_setup(self):
        settings = info()
        self.assertEqual(settings['engine'], 'SQLite')
        self.assertEqual(settings['is_sqlite'], True)


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username=TEST_USERNAME,
                                   email=TEST_EMAIL,
                                   dob=TEST_DOB)
        user.set_password(TEST_PASSWORD)
        # need to save after setting password
        user.save()

    def test_users_count(self):
        """Check that we have 1 user in test DB"""

        n_users = User.objects.all().count()
        self.assertEqual(n_users, 1)

    def test_user_password_set(self):
        """Check that password for user has been set"""

        user = auth.authenticate(username=TEST_USERNAME, password=TEST_PASSWORD)
        self.assertIsNotNone(user)


class GetSignup(TestCase):
    def test_ok(self):
        signup_url = reverse_lazy("signup")
        response = self.client.get(signup_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "hobbies/signup.html")


class PostSignup(TestCase):
    def test_signupworks(self):
        # Get CSRF token
        signup_url = reverse_lazy("signup")
        response = self.client.get(signup_url, follow=True)
        self.assertContains(response, 'csrfmiddlewaretoken')
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token_input = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})

        data = CREDS.copy()
        data["username"] = TEST_USERNAME2
        data["password_confirmation"] = TEST_PASSWORD
        data["dob"] = TEST_DOB.strftime("%Y-%m-%d")
        data['csrfmiddlewaretoken'] = csrf_token_input['value']

        response = self.client.post("/signup/", data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertTemplateUsed(response, 'hobbies/index.html')

        # new user was actually created
        all_users = User.objects.all()
        new_user = User.objects.filter(username=TEST_USERNAME2)
        self.assertEquals(len(new_user), 1)


class GetLogin(TestCase):
    def setUp(self):
        User.objects.create_user(**CREDS)

    def test_ok(self):
        login_url = reverse_lazy("login")
        response = self.client.get(login_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "hobbies/login.html")

    def test_loginworks(self):
        # Get CSRF token
        login_url = reverse_lazy("login")
        response = self.client.get(login_url)
        self.assertContains(response, 'csrfmiddlewaretoken')
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token_input = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})

        data = CREDS.copy()
        data['csrfmiddlewaretoken'] = csrf_token_input['value']

        response = self.client.post(login_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertTemplateUsed('hobbies/login.html')
        self.assertTemplateUsed('hobbies/index.html')
