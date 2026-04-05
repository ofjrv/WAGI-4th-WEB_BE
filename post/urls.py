# post/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('write/', views.write, name='write'),
    path('detail/<int:post_id>/', views.detail, name='detail'),
    path('update/<int:post_id>/', views.update, name='update'), # [추가 확인]
    path('delete/<int:post_id>/', views.delete, name='delete'),
]