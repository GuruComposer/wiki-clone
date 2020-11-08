from django.urls import include, path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("wiki/<str:title>/edit", views.edit, name="edit")
]
