from django.db import models
from django.conf import settings  # 유저 모델 참조를 위해 필요
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 좋아요: User 모델과 다대다(M:N) 관계
    likes = models.ManyToManyField(User, related_name='like_posts', blank=True)

    def __str__(self):
        return self.title

# 여러 이미지를 저장하기 위한 모델 (Post와 N:1 관계)
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

# PostImage 삭제 시 실제 파일도 서버에서 삭제하는 로직
@receiver(post_delete, sender=PostImage)
def post_image_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

# [추가] 댓글 모델: Post와 1:N 관계
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # [대댓글 핵심] 자기 자신을 참조하는 parent 필드
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.author.username}의 댓글"