from rest_framework import permissions

from reviews.models import User


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == User.ADMIN
