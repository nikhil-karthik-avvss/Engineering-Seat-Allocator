from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('home/',include("account.urls")),
    path('institute_home/',include("institute.urls")),
    path('emailenter/',views.emailenter,name="emailenter"),
    path('student_login/',views.student_login,name="student_login"),
    path('institute_login/',views.institute_login,name="institute_login"),
    path('emailenter/email_verify/',views.email_verify,name="email_verify"),
    path('emailenter/email_verify/verify_otp/',views.verify_otp,name="verify_otp"),
    path('emailenter/email_verify/verify_otp/register/',views.register_db,name="register_db"),
    path('pass_enter/',views.pass_enter, name="pass_enter"),
    path('pass_enter/reset_password/',views.reset_password,name="reset_password")
    #path('pass_enter/pass_enter/',views.pass_enter,name="pass_enter")
]
