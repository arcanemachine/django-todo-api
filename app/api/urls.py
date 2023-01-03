from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api import views

app_name = "api"

router = routers.SimpleRouter()  # trailing_slash=False)
router.register(r"todos", views.TodoViewSet, basename="todos")
# router.register(r"users", views.UserViewSet, basename="users")

urlpatterns = router.urls + [
    # auth
    path("", views.api_root, name="api_root"),
    # auth
    path("auth/check/", views.user_auth_status_check, name="user_auth_status_check"),
    path("auth/login/token/", obtain_auth_token, name="login_token"),
    path("auth/login/session/", views.SessionLoginView.as_view(), name="login_session"),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    # utility
    path(
        "utils/csrfmiddlewaretoken/",
        views.Csrfmiddlewaretoken.as_view(),
        name="csrfmiddlewaretoken",
    ),
    # schema
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="api:schema"),
        name="redoc",
    ),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger_ui",
    ),
]
