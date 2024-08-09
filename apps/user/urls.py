from django.urls import path
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('sign-up/', sign_up, name='sign_up'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]