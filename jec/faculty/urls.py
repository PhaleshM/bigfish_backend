from django.urls import path
from . import views
urlpatterns = [
    path('',views.FacultyData,name="FacultyData"),
]