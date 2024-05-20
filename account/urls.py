from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('seatmatrix/',views.view_sm,name="view_sm"),
    path('ranklist/',views.view_crl,name="view_crl"),
    path('choice/',views.choice,name="choice"),
    path('get_college_name/', views.get_college_name, name='get_college_name'),
    path('get_programs/', views.get_programs, name='get_programs'),
    path('logout/',views.logout_stud,name='logout_stud')
]
