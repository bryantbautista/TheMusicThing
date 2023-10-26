from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("helloworld2", views.helloworld2, name="helloworld2"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/logout", views.logoutaccount, name="logout")
]