from django.test import TestCase
from home.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestUserRegistrationForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Load initial data for the TestCase."""
        User.objects.create_user(username='kevin', email='kevin@email.com', password='kevinpass')

    def test_valid_data(self):
        form = UserRegistrationForm(
            dict(username='ali', email='ali@email.com', password1='alipass', password2='alipass'))
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(dict())
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exists_email(self):
        form = UserRegistrationForm(
            dict(username='notkevin', email='kevin@email.com', password1='kevinpass', password2='kevinpass'))
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))

    def test_unmatched_passwords(self):
        form = UserRegistrationForm(
            dict(username='mark', email='mark@email.com', password1='mark', password2='markkkk'))
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)
