from django.db import models
from django.conf import settings  # 유저 모델 참조를 위해 필요
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Post(models.Model):
    # [4주차 핵심] 유저 모델과 1:N 관계 설정
    # 유저가 삭제되면 해당 유저의 글도 삭제되도록 CASCADE 설정
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # 시간 기록 필드
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

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