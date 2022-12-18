from django.conf import settings
from django.db import models


class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
