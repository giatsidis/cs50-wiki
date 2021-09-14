from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("save_entry", views.save_entry, name="save_entry"),
    path("save_entry/<str:title>", views.save_entry, name="save_edited_entry"),
    path("edit_entry/<str:title>", views.edit_entry, name="edit_entry"),
    path("random", views.random_entry, name="random_entry")
]
