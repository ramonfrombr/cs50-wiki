from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path('new_page/', views.new_page, name="new_page"),
    path("edit_page/<str:page>/", views.edit_page, name="edit_page"),
    path("<str:page>/", views.page, name="page"),
    path("403", views.not_allowed, name="not_allowed"),
    path("random_page", views.random_page, name="random_page")
]
