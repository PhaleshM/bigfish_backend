from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required, permission_required
from .models import StudentProfile, ProfessorProfile, User

@login_required
def ProfileView(request):
    role=User.objects.get(username=request.user).role
    print(role,request.user)
    if role=="STUDENT":
        data=StudentProfile.objects.get(rollno=request.user)
    else:
        data= ProfessorProfile.objects.get(user=request.user)
    context={
        "data":data,
        "role":role
    }
    
    return render(request, "user/profile.html", context)
    
def home_view(request):
    return render(request,'index.html',{'title':'Home'})

# class LoginViewUser(LoginView):
#     template_name="user/login.html"

    