from django.test import TestCase
from user.models import Feeling
from django.contrib.auth.models import User

# Create your tests here.
class Test(TestCase):
    def test_user_info(self):
        response = self.client.get('/user/info/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/user/info/')

    def test_user_not_found(self):
        response = self.client.get('/user/user-not-found')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_not_found.html')

    def test_user_info_with_login(self):
        u = User.objects.create_user(username='test', password='test')
        self.client.login(username='test', password='test')
        response = self.client.get('/user/info/')
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        response = self.client.get('/user/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)
        
