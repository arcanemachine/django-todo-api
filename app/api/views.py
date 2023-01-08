from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.urls import reverse
from push_notifications.models import GCMDevice
from rest_framework import permissions as drf_permissions
from rest_framework import views, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api import serializers
from todos.models import Todo

UserModel = get_user_model()


# MIXINS #
class CrsfRequiredApiViewMixin(views.APIView):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.csrf_exempt = False
        return view


# VIEWS #
def api_root(request):
    """Show all available API documentation."""

    host = f"{request.scheme}://{request.get_host()}"
    return JsonResponse(
        {
            "schema": host + reverse("api:schema"),
            "redoc": host + reverse("api:redoc"),
            "swagger_ui": host + reverse("api:swagger_ui"),
        }
    )


# auth
class AuthStatusCheckSession(GenericAPIView):
    """Check if a user is authenticated using session authentication."""

    permission_classes = [drf_permissions.AllowAny]
    serializer_class = serializers.DrfAuthtokenSerializer
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        return JsonResponse(request.user.is_authenticated, safe=False)


class AuthStatusCheckToken(AuthStatusCheckSession):
    """Check if a user is authenticated using token authentication."""

    authentication_classes = [TokenAuthentication]


class GCMDeviceViewSet(viewsets.ModelViewSet):
    """
    Register a device with Firebase Cloud Messaging (FCM).
    """

    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.GCMDeviceSerializer
    queryset = GCMDevice.objects.all()  # drf_spectacular: allow automatic introspection

    def get_object(self):
        registration_id = self.request.data["registration_id"]
        user = self.request.user

        return get_object_or_404(GCMDevice, registration_id=registration_id, user=user)


class TokenLogin(ObtainAuthToken):
    """Login using token authentication."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [drf_permissions.AllowAny]


class SessionLogin(LoginView):
    """Login using session authentication."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [drf_permissions.AllowAny]


# todos
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()  # drf_spectacular: allow automatic introspection
    serializer_class = serializers.TodoSerializer

    def get_queryset(self):
        """Return all todos that belong to the user."""
        return Todo.objects.filter(user=self.request.user)


# # users
# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = [drf_permissions.IsAuthenticated]
#     queryset = UserModel.objects.all()
#     serializer_class = serializers.UserSerializer


# utility
class Csrfmiddlewaretoken(CrsfRequiredApiViewMixin, views.APIView):
    serializer_class = serializers.CsrfmiddlewaretokenSerializer
    permission_classes = [drf_permissions.AllowAny]

    def get(self, request):
        # issue a new CSRF token
        data = {"csrfmiddlewaretoken": get_token(request)}
        serializer = serializers.CsrfmiddlewaretokenSerializer(data=data)

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response({"message": "Could not create csrfmiddlewaretoken"})

    def post(self, request, *args, **kwargs):
        # check if the user's CSRF token is valid (it is always safe to return True
        # here because the CSRF middleware will catch any unauthorized requests)
        return JsonResponse(True, safe=False)
