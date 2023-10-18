from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login_view"),
    path("logout/",views.logout_view,name="logout_view"),
    path("profile/",views.profile,name="profile"),
    path("verifyOTP",views.verifyOTP,name="verifyOTP"),
    path("reset_pass",views.reset_pass,name="reset_pass"),
    path("get_email",views.get_email,name="get_email"),
    path("findMatch",views.findMatch,name="findMatch"),
    path("user_profile/<str:username>/",views.user_profile,name="user_profile"),
]