from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('institute_home/',views.institute_home,name="institute_home"),
    path('profile/',views.profile,name="profile"),
    path('seatmatrix_input/',views.seatmatrix_input,name="seatmatrix_input"),
    path('seatmatrix_success/', views.seatmatrix_success, name="seatmatrix_success"),
    path('logout/',views.logout,name="logout")
    #path('institute_login/',include("pages.urls")),
]
