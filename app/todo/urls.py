from django.contrib import admin
from django.urls import include, path

api_auth_prefix = "api/auth"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path(
        "api/auth/",
        include("dj_rest_auth.urls"),
    ),
    path(
        "api/auth/registration/",
        include("dj_rest_auth.registration.urls"),
    ),
    path(
        "api/auth/native/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
]
