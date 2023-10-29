from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user:register')
        self.login_url = reverse('user:login')

    def test_register_POST(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testing321',
            'password2': 'testing321'
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'success': True})


    def test_login_user_POST(self):
        self.user = User.objects.create_user(username='testuser', password='testing321')
        
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testing321',
            'feeling': 'HA'
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'success': True})
