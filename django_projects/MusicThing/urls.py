from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logoutView, name="logout"),
    path("login", views.loginView, name="login"),
    path("register", views.registerView, name="register"),
    path("home", views.homeView, name="home")
]
