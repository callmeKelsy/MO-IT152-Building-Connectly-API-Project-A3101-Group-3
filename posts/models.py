from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    def set_default_password(self):
        """Sets a default password if none is provided."""
        if not self.password or not self.has_usable_password():
            self.set_password('defaultpassword123')
            self.save()

# Post model with post types and foreign key to User (author)
class Post(models.Model):
    class PostTypes(models.TextChoices):
        TEXT = 'text', 'Text'
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=10, choices=PostTypes.choices, default=PostTypes.TEXT)
    metadata = models.JSONField(default=dict)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Comment model with foreign keys to User (author) and Post (post)
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.title}"
