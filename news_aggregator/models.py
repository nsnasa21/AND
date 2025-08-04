from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    class Meta:
        unique_together = ('name', 'category')

class Keyword(models.Model):
    text = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='keywords')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.topic.name} - {self.text}"
    
    class Meta:
        unique_together = ('text', 'topic')

class APISetting(models.Model):
    name = models.CharField(max_length=50, unique=True)
    api_key = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class RSSFeed(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    url = models.URLField(unique=True)
    source = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    is_duplicate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional profile fields here
    
    def __str__(self):
        return f"{self.user.username}'s profile"
