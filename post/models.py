from django.db import models

# post/models.py
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # upload_to를 비우면 C:/django_media/ 바로 아래에 저장됩니다.
    image = models.ImageField(upload_to='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title