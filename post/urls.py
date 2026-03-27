from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('write/', views.write, name='write'),
    path('list/', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
]