from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post
from rest_framework.authtoken.models import Token


User = get_user_model()  # Ensure we're using the correct User model


class CreatePostViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

    def test_create_post_success(self):
        url = reverse("create_post")  # Ensure this name matches your URL conf
        response = self.client.post(url, {"title": "Test Post", "content": "This is a test."}, format="json")
        self.assertEqual(response.status_code, 201)


class PostPermissionsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpassword", email="admin@example.com")
        self.regular_user = User.objects.create_user(username="regularuser", password="userpassword")

        # Create authentication tokens
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.regular_token = Token.objects.create(user=self.regular_user)

        # Create posts
        self.post_by_regular_user = Post.objects.create(
            title="Regular User's Post",
            content="This is a post created by a regular user.",
            author=self.regular_user,
        )
        self.post_by_admin = Post.objects.create(
            title="Admin User's Post",
            content="This is a post created by the admin.",
            author=self.admin_user,
        )

    def test_regular_user_can_edit_own_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.regular_token.key}")

        url = f"/api/posts/{self.post_by_regular_user.id}/"
        data = {"title": "Updated Regular User Post", "content": "This is an updated post."}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post_by_regular_user.refresh_from_db()
        self.assertEqual(self.post_by_regular_user.title, "Updated Regular User Post")

    def test_regular_user_cannot_edit_other_users_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.regular_token.key}")

        url = f"/api/posts/{self.post_by_admin.id}/"
        data = {"title": "Updated Admin Post", "content": "This is an updated post."}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_edit_any_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        url = f"/api/posts/{self.post_by_regular_user.id}/"
        data = {"title": "Updated by Admin", "content": "This post is updated by the admin."}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post_by_regular_user.refresh_from_db()
        self.assertEqual(self.post_by_regular_user.title, "Updated by Admin")

    def test_regular_user_cannot_delete_other_users_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.regular_token.key}")

        url = f"/api/posts/{self.post_by_admin.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_any_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        url = f"/api/posts/{self.post_by_regular_user.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Post.DoesNotExist):
            self.post_by_regular_user.refresh_from_db()

    def test_regular_user_can_delete_own_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.regular_token.key}")

        url = f"/api/posts/{self.post_by_regular_user.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Post.DoesNotExist):
            self.post_by_regular_user.refresh_from_db()
