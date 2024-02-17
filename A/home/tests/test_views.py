from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from home.views import Home
from home.forms import UserRegistrationForm


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        response = self.client.get(reverse('home:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/register.html')
        self.failUnless(response.context['form'], UserRegistrationForm)

    def test_user_register_POST_valid(self):
        response = self.client.post(reverse('home:user_register'),
                                    data={'username': 'kevin', 'email': 'kevin@email.com', 'password1': 'kevinpass',
                                          'password2': 'kevinpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_POST_invalid(self):
        response = self.client.post(reverse('home:user_register'),
                                    data={'username': 'kevin', 'email': 'invalid email', 'password1': 'kevinpass',
                                          'password2': 'kevinpass'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response.context['form'], 'email', ['Enter a valid email address.', ])


class TestWriterView(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', email='john@email.com', password='johnpass')
        self.client = Client()
        self.client.login(username='john', email='john@email.com', password='johnpass')

    def test_writers_GET(self):
        response = self.client.get(reverse('home:writers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/writers.html')


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='root', email='root@email.com', password='rootpass')
        self.factory = RequestFactory()

    def test_home_user_authenticated(self):
        request = self.factory.get(reverse('home:home'))
        request.user = self.user
        response = Home.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_home_user_anonymous(self):
        request = self.factory.get(reverse('home:home'))
        request.user = AnonymousUser()
        response = Home.as_view()(request)
        self.assertEqual(response.status_code, 200)
