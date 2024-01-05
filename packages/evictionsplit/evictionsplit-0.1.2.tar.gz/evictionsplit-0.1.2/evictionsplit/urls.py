from django.urls import path

from . import views

app_name = "evictionsplit"

urlpatterns = [
    path("", views.index, name="index"),
    path("list", views.list_evictions, name="list"),
    path("new", views.new_eviction, name="new"),
    path("apply/<int:id>", views.apply, name="apply"),
    path("eviction/<int:id>", views.eviction, name="eviction"),
    path(
        "eviction/<int:eviction_id>/clocking",
        views.change_clocking,
        name="change_clocking",
    ),
    path(
        "eviction/<int:eviction_id>/apply/<int:user_id>",
        views.accept_application,
        name="accept_application",
    ),
    path("eviction/management", views.management, name="manage"),
    path("eviction/<int:eviction_id>/stop", views.stop_eviction, name="stop_eviction"),
]
