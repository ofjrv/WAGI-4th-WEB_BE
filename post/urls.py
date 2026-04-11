from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'post'

urlpatterns = [
    path('', views.list, name='list'),
    path('write/', views.write, name='write'),
    path('<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.update, name='update'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]