from django.contrib.auth import get_user_model
from push_notifications.models import GCMDevice
from rest_framework import serializers

from todos.models import Todo

UserModel = get_user_model()


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "content", "is_completed"]

    def create(self, validated_data):
        user = self.context["request"].user
        # user = UserModel.objects.first()
        todo = Todo.objects.create(user=user, **validated_data)
        return todo


class CsrfmiddlewaretokenSerializer(serializers.Serializer):
    csrfmiddlewaretoken = serializers.CharField(max_length=64, write_only=True)


class GCMDeviceSerializer(serializers.ModelSerializer):
    registration_id = serializers.CharField(label="FCM Device Token", write_only=True)

    class Meta:
        model = GCMDevice
        fields = ["registration_id"]

    def create(self, validated_data):
        registration_id = validated_data["registration_id"]
        user = self.context["request"].user

        # check if device is already registered (if so, return the existing object)
        existing_device = GCMDevice.objects.filter(
            registration_id=registration_id,
            user=user,
        ).first()
        if existing_device is not None:
            return existing_device

        # TODO: set old devices as inactive if too many devices created
        gcmdevice = GCMDevice.objects.create(
            user=user,
            cloud_message_type="FCM",
            **validated_data,
        )

        # send a test message to ensure the token is valid
        # (this code should be run asynchronously to avoid network bottlenecks)
        response = gcmdevice.send_message("Welcome to Todo List!")
        if (
            "error" in response["results"][0]
            and response["results"][0]["error"] == "InvalidRegistration"
        ):
            raise serializers.ValidationError(
                {"registration_id": "Invalid FCM device token."}
            )

        return gcmdevice


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ["id", "username"]
