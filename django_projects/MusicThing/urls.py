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
    path("postComment/<slug:albumID>", views.postComment, name="postComment"),
    path("FAQ/", views.FAQView, name="FAQ"),
    path("support", views.supportView, name="support"),
    path("feedback_submission/", views.feedback_submission, name="feedback_submission"),
    path("charts", views.chartsView, name="charts"),
    path("random", views.randomView, name="random"),
    path("profile/<slug:username>", views.profileView, name="profile"),
    path("profile/<slug:username>/<int:page>", views.profileNextPage, name="profilenextpage"),
    path("search", views.searchView, name="search"),
    path("explore", views.exploreView, name="explore"),
    path("delete/<slug:albumID>/<slug:commentID>", views.deleteView, name="delete")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
