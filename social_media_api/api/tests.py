from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Post, Follow

class UserTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.user.save()

    def test_user_login(self):
        # Test that the user can log in with valid credentials
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        # Test invalid login
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Invalid credentials")


class PostTests(APITestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.post = Post.objects.create(content="Test post", author=self.user)

    def test_create_post(self):
        # Test that a user can create a post
        response = self.client.post('/api/posts/', {'content': 'New post content'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)  # Verify post count increased by 1

    def test_view_post(self):
        # Test viewing a post
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test post')

    def test_delete_post(self):
        # Test deleting a post
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)  # Verify post is deleted


class FollowTests(APITestCase):
    def setUp(self):
        # Create two users for testing the follow system
        self.user1 = CustomUser.objects.create_user(username='user1', password='password1')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password2')
        self.client.login(username='user1', password='password1')

    def test_follow_user(self):
        # Test following functionality
        response = self.client.post('/api/follows/', {'followed_user': self.user2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user1.following.filter(followed_user=self.user2).exists())

    def test_follow_self(self):
        # Test that users cannot follow themselves
        response = self.client.post('/api/follows/', {'followed_user': self.user1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "You cannot follow yourself.")
