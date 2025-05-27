# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='login'),
    path('register/', views.student_register, name='register'),
    path('logout/', views.student_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/update/', views.profile_update, name='profile_update'),
    
    # Add these missing URL patterns
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
]