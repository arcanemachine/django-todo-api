from rest_framework import viewsets

from api import serializers
from todos.models import Todo


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TodoSerializer
    queryset = Todo.objects.all()
