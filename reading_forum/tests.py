from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from reading_forum.models import Discussion, Reply
from reading_forum.forms import DiscussionForm, ReplyForm


class DiscussionViewsTest(TestCase):
    def setUp(self):
        #test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        #create sample
        self.discussion = Discussion.objects.create(title='Test Discussion', user=self.user)
        self.reply = Reply.objects.create(content='Test Reply', discussion=self.discussion, user=self.user)

    def test_discussion_list_view(self):
        response = self.client.get(reverse('reading_forum:discussion_list'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussion_list.html')

    def test_discussion_detail_view(self):
        response = self.client.get(reverse('reading_forum:discussion_detail', args=[self.discussion.id]))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussion_detail.html')

    def test_create_discussion_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('reading_forum:create_discussion'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussion_form.html')

    def test_create_reply_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('reading_forum:discussion_detail', args=[self.discussion.id]))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussion_detail.html')


    def test_reply_form_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('reading_forum:reply_form', args=[self.discussion.id]))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reply_form.html')

    def test_reply_form_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('reading_forum:reply_form', args=[self.discussion.id]), {'content': 'Test Reply'})  
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('reading_forum:discussion_detail', args=[self.discussion.id]))

    def test_create_discussion_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('reading_forum:create_discussion'), {'title': 'Test Discussion', 'content': 'Test Content'})  
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('reading_forum:discussion_list'))

    def test_create_discussion_view_post_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('reading_forum:create_discussion'), {'title': '', 'content': ''})  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussion_form.html')

    def test_without_login(self):
        response = self.client.get(reverse('reading_forum:create_discussion'))  
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/reading_forum/create-discussion/')

    def test_without_login_reply(self):
        response = self.client.get(reverse('reading_forum:reply_form', args=[self.discussion.id]))  
        self.assertEqual(response.status_code, 200)