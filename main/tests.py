from django.test import TestCase, Client

# Create your tests here.
class mainTest(TestCase):
    def test_search_url_is_exist(self):
        response = Client().get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_using_search_template(self):
        response = Client().get('/search/')
        self.assertTemplateUsed(response, 'search_form.html')