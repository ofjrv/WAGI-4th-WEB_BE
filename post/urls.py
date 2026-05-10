from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('write/', views.write, name='write'),
    path('detail/<int:post_id>/', views.detail, name='detail'),
    path('update/<int:post_id>/', views.update, name='update'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    
    path('like/<int:post_id>/', views.post_like, name='post_like'),
    path('comment/like/<int:comment_id>/', views.comment_like, name='comment_like'),
    path('comment/<int:post_id>/', views.comment_write, name='comment_write'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),

]