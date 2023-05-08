from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('content_creator', 'Content Creator'),
    )

    role = models.CharField(max_length=50, choices=USER_ROLES, default='content_creator')
    def __str__(self):
        return self.username

class Blog(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='images/')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

