from rest_framework import permissions


class HasTodoReadPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user is request.user
