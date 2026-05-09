from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.list, name='list'),
    path('write/', views.write, name='write'),
    path('<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.update, name='update'),
    path('<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:pk>/like/', views.post_like, name='post_like'),
    path('comment/<int:comment_pk>/reply/', views.reply_create, name='reply_create'),
    path('comment/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
]