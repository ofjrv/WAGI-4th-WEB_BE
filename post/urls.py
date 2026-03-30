from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('write/', views.write, name='write'),
    path('detail/<int:post_id>/', views.detail, name='detail'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
]