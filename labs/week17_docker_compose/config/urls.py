"""Root URL configuration — provided."""

from django.urls import path

from healthcheck.views import healthz

urlpatterns = [
    path("healthz/", healthz, name="healthz"),
]
