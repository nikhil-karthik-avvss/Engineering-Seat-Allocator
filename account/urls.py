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
    path('logout/',views.logout_stud,name='logout_stud'),
    path('view_allotment_stud',views.view_allotment_stud,name='view_allotment_stud'),
    path('update_allotment/', views.update_allotment, name='update_allotment'),
    path('view_manual/',views.view_manual,name='view_manual'),
    path('institutes/', views.college_list, name='college_list'),
    path('institutes/<int:college_id>/', views.college_detail, name='college_detail'),
    path('prev_allotment/',views.prev_allotment,name='prev_allotment'),
    path('curr_allotment/',views.curr_allotment,name='curr_allotment'),
]
