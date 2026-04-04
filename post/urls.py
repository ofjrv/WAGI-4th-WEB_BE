from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.list, name='list'),
    path('write/', views.write, name='write'),
    path('<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.update, name='update')
]