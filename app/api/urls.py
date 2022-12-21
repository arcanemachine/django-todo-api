from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api import views

app_name = "api"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"todos", views.TodoViewSet, basename="todo")
# router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = router.urls + [
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="api:schema"),
        name="redoc",
    ),
    # utility
    path(
        "utils/csrf/get",
        views.csrf_get,
        name="csrf_get",
    ),
    path(
        "utils/csrf/check",
        views.csrf_check,
        name="csrf_check",
    ),
]
