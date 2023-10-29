from django.contrib.auth.models import User
from django.test import TestCase, Client
from main.models import Profile
from django.urls import reverse

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

    def test_profile_exist(self):
                user = User.objects.create_user(username='testuser', password='12345')
                profile = Profile.objects.create(user=user)
                profile_exist = Profile.objects.filter(user=user).exists()
                self.assertTrue(profile_exist)

    def test_profile_not_found(self):
            response = Client().get('/user/info/unknown/')
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, '/user/user-not-found')
