from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)  
    email = models.EmailField(unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  
    title = models.CharField(max_length=200)  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title

