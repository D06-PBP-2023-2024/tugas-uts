from django.test import TestCase, Client
from main.models import Profile
from django.contrib.auth.models import User

class ProfileModelTest(TestCase):
        def test_profile_exist(self):
                user = User.objects.create_user(username='testuser', password='12345')
                profile = Profile.objects.create(user=user)
                profile_exist = Profile.objects.filter(user=user).exists()
                self.assertTrue(profile_exist)

        def test_profile_not_found(self):
                response = Client().get('/user/info/unknown/')
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, '/user/user-not-found')