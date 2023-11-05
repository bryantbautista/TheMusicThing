from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logoutView, name="logout"),
    path("login", views.loginView, name="login"),
    path("register", views.registerView, name="register"),
    path("home", views.homeView, name="home")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
