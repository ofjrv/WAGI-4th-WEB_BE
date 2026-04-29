from django.urls import path
from . import views

urlpatterns = [
    # 게시판 기본 기능
    path('', views.home, name='home'),
    path('write/', views.write, name='write'),
    path('detail/<int:post_id>/', views.detail, name='detail'),
    path('update/<int:post_id>/', views.update, name='update'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    
    # [5주차 추가] 좋아요 & 댓글 기능 (이 부분이 추가되어야 에러가 안 납니다!)
    path('like/<int:post_id>/', views.post_like, name='post_like'),
    path('comment/<int:post_id>/', views.comment_write, name='comment_write'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),

    # 계정 관련 - 직접 구현한 뷰 연결
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]