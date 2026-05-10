from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('write/', views.write, name = 'write'),
    path('detail/<int:post_id>/', views.detail, name='detail'),
    path('update/<int:id>/', views.update, name='update'),
    path('comment/<int:post_id>/', views.create_comment, name='create_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/like/<int:comment_id>/', views.comment_like, name='comment_like')
]