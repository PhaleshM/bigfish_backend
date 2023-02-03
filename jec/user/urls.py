# from django.urls import path
# from .views import LoginViewUser
# urlpatterns = [
#     path("login/",LoginViewUser.as_view(),"login")
# ]

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# from accounts import views
from .views import ProfileView

urlpatterns = [
    path('profile/', ProfileView, name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]