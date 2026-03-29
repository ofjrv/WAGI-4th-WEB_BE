from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200) # 제목
    content = models.TextField()               # 본문
    image = models.ImageField(upload_to='posts/', blank=True, null=True) # 단일 이미지
    created_at = models.DateTimeField(auto_now_add=True) # 작성일

    def __str__(self):
        return self.title