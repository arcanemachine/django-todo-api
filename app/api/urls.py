from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api import views

app_name = "api"

router = routers.SimpleRouter()  # trailing_slash=False)
router.register(r"todos", views.TodoViewSet, basename="todos")
# router.register(r"users", views.UserViewSet, basename="users")

urlpatterns = router.urls + [
    path("", views.api_root, name="api_root"),
    # auth
    path("auth/check/", views.auth_status_check, name="auth_status_check"),
    path("auth/login/", views.SessionLogin.as_view(), name="login_session"),
    path("auth/login/token/", views.ProjectObtainAuthToken.as_view(), name="login"),
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
