from django.contrib import admin
from django.urls import path, include
from django.conf import settings # [추가] 설정값을 쓰기 위해 필요
from django.conf.urls.static import static # [추가] 정적 파일을 서빙하기 위해 필요

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('post.urls')),
]

# if 문은 urlpatterns 리스트 밖(아래쪽)에 따로 적어야 합니다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)