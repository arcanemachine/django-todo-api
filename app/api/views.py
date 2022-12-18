from rest_framework import permissions, viewsets

from api import serializers
from todos.models import Todo


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TodoSerializer
    queryset = Todo.objects.all()  # allow automatic introspection for drf_spectacular

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = UserModel.objects.all()
#     serializer_class = serializers.UserSerializer
#     permission_classes = [drf_permissions.IsAdminUser]
