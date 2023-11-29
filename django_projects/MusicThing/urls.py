from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.homeView, name="home"),
    path("logout", views.logoutView, name="logout"),
    path("login", views.loginView, name="login"),
    path("register", views.registerView, name="register"),
    path("album/<slug:albumID>", views.albumView, name="album"),
    path("updateRating/<slug:albumID>", views.updateRating, name="updateRating"),
    path("charts", views.chartsView, name="charts"),
    path("random", views.randomView, name="random")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
