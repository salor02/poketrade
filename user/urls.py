from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'user'

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("account/<int:user_id>/detail", UserDetailView.as_view(), name='account_detail'),
    path("account/edit", ProfileUpdateView.as_view(), name='account_edit')
]