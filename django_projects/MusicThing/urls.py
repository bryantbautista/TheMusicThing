from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("helloworld2", views.helloworld2, name="helloworld2")
]