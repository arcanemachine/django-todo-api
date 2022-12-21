from django.http import JsonResponse
from django.middleware.csrf import get_token

# from django.contrib.auth import get_user_model
from rest_framework import permissions as drf_permissions
from rest_framework import viewsets

from api import serializers
from todos.models import Todo

# UserModel = get_user_model()


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [drf_permissions.IsAuthenticated]
    queryset = Todo.objects.all()  # allow automatic introspection for drf_spectacular
    serializer_class = serializers.TodoSerializer

    def get_queryset(self):
        """Return all todos that belong to the user."""
        return Todo.objects.filter(user=self.request.user)


# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = [drf_permissions.IsAuthenticated]
#     queryset = UserModel.objects.all()
#     serializer_class = serializers.UserSerializer


# utility
def csrf_get(request):
    return JsonResponse({"csrftoken": get_token(request)})


def csrf_check(request):
    return JsonResponse({"result": "OK"})
