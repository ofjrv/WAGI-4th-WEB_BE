from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('write/', views.write, name='write'),
    path('detail/<int:id>/', views.detail, name='detail'),
]