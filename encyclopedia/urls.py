from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.site, name="site"),
    path("new_page", views.new, name="new_page"),
    path("edit_page/<str:title>", views.edit, name="edit_page"),
    path("random_page", views.random_page, name="random_page")
]
