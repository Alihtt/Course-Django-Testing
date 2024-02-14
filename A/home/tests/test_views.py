from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
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
