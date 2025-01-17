from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)  # User's unique username
    email = models.EmailField(unique=True)  # User's unique email
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user was created

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  # Related to User
    title = models.CharField(max_length=200)  # Post title
    content = models.TextField()  # Post content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created

    def __str__(self):
        return self.title

