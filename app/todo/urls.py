from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("dj-admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
