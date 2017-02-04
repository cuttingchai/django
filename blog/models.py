from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=80)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.first_name
    
    
class Comment(models.Model):
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.author.first_name + "commented"