from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)      # 글 제목
    content = models.TextField()                    # 글 본문
    image = models.ImageField(upload_to='post/', blank=True, null=True) # 이미지 (선택사항)
    created_at = models.DateTimeField(auto_now_add=True) # 작성일 자동 저장

    def __str__(self):
        return self.title
    