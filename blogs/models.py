from django.db import models

class BlogPost(models.Model):
    """An entry in a blog"""
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64, unique=True)
    text = models.TextField(max_length=400)
    #remember to add a user
    
    def __str__(self):
        return f"{self.title}"