from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.urls import reverse
from rest_framework import permissions as drf_permissions
from rest_framework import views, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api import serializers
from todos.models import Todo

UserModel = get_user_model()


def api_root(request):
    host = f"{request.scheme}://{request.get_host()}"
    return JsonResponse(
        {
            "schema": host + reverse("api:schema"),
            "redoc": host + reverse("api:redoc"),
            "swagger_ui": host + reverse("api:swagger_ui"),
        }
    )


# auth
class CrsfRequiredApiView(views.APIView):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.csrf_exempt = False
        return view


class SessionLoginView(LoginView):
    pass


def user_auth_status_check(request):
    return JsonResponse(request.user.is_authenticated, safe=False)


# todos
class TodoViewSet(viewsets.ModelViewSet):
    # permission_classes = [drf_permissions.IsAuthenticated]
    permission_classes = [drf_permissions.AllowAny]
    queryset = Todo.objects.all()  # allow automatic introspection for drf_spectacular
    serializer_class = serializers.TodoSerializer

    # def post(self, request, *args, **kwargs):
    #     breakpoint()

    # def get_queryset(self):
    #     """Return all todos that belong to the user."""
    #     return Todo.objects.filter(user=self.request.user)


# # users
# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = [drf_permissions.IsAuthenticated]
#     queryset = UserModel.objects.all()
#     serializer_class = serializers.UserSerializer


# utility
class Csrfmiddlewaretoken(CrsfRequiredApiView, GenericAPIView):
    serializer_class = serializers.CsrfmiddlewaretokenSerializer
    permission_classes = [drf_permissions.AllowAny]

    def get(self, request, *args, **kwargs):
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
