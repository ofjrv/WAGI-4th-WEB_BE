from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # [추가] auto_now_add는 생성 시에만, auto_now는 수정 시마다 기록됩니다.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

# [핵심] 여러 이미지를 저장하기 위한 모델 (1:N 관계)
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

# [수정] PostImage가 삭제될 때 실제 파일도 삭제되도록 설정
@receiver(post_delete, sender=PostImage)
def post_image_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)