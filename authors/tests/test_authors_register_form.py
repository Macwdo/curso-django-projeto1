from unittest import TestCase

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterForm(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your email'),
        ('first_name', 'Your first name'),
        ('last_name', 'Your last name'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password')
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        test_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, test_placeholder)

    @parameterized.expand([
        ('username', ("Your username must be greater than 4 characters and less 150. Letters, numbers and @/./+/-/_ only.")),
        ('password', ("Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.")),
        ('email', 'Please Insert a valid E-mail'),
        ('password2', 'This field must be equal password field')
    ])
    def test_help_text(self, field, needed):
        form = RegisterForm()
        test_placeholder = form[field].field.help_text
        self.assertEqual(needed, test_placeholder)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-Mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Repeat your pass')
    ])
    def test_labels(self, field, needed):
        form = RegisterForm()
        test_placeholder = form[field].field.label
        self.assertEqual(needed, test_placeholder)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'email': 'user@email.com',
            'last_name': 'lastn',
            'first_name': 'firstn',
            'password': 'Danilo21@',
            'password2': 'Danilo21@'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Repeat your password'),
        ('email', 'Email is required')

    ])
    def test_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.content.decode('utf-8'))

    def test_user_field_min_length_should_be_4(self):
        self.form_data['username'] = 'seo'
        url = reverse('authors:register_create')
        msg = "Your password must be greater than 4 characters"
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_user_field_max_length_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:register_create')
        msg = "Your password must be less 150 characters"
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = 'Bomdia123'
        self.form_data['password2'] = 'Bomdias123'
        url = reverse('authors:register_create')
        msg = "Please insert equal passwords"
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_return_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = "User e-mail is already in use"
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'testuser',
            'password': 'Danilo21@',
            'password2': 'Danilo21@'
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username='testuser',
            password='Danilo21@',
        )
        self.assertTrue(is_authenticated)
