from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from rest_framework import serializers

from todos.models import Todo

UserModel = get_user_model()


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "content", "is_completed"]

    def create(self, validated_data):
        # user = self.context["request"].user
        user = UserModel.objects.first()
        todo = Todo.objects.create(user=user, **validated_data)
        return todo


class CsrfmiddlewaretokenSerializer(serializers.Serializer):
    csrfmiddlewaretoken = serializers.CharField(max_length=64)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ["id", "username"]
