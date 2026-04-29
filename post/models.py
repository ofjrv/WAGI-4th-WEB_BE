from django.conf import settings 
from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. 유저 모델 (AbstractUser 상속)
class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

# 2. 게시글 모델
class Post(models.Model):
    title = models.CharField(max_length=200)      
    content = models.TextField()                    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    likes = models.ManyToManyField(User, related_name='like_posts', blank=True)
    
    def __str__(self):
        return self.title

# 3. 이미지 모델 
class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

# 4. 댓글 모델 추가
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}의 댓글: {self.content[:10]}"