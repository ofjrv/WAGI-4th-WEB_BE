from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# [수정] 프로젝트 루트에는 views가 없으므로 post 앱에서 가져옵니다.
from post import views as post_views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('post.urls')), # post 앱의 urls.py를 포함
    
    # 로그인/로그아웃 (장고 내장 뷰 활용)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # 최근 장고 버전은 로그아웃을 POST로 처리하므로 아래처럼 설정합니다.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 회원가입 (post 앱의 views에 만든 signup 함수 연결)
    path('signup/', post_views.signup, name='signup'),
]

# 미디어 파일 서빙 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)