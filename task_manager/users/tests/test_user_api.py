# users/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import RegisterUser

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse('users')  # Correct view name is 'users'
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'name': 'Test User',
            'phone_number': '1234567890',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('jwt', response.data)
