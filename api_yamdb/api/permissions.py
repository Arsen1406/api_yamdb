from rest_framework import permissions

from reviews.models import User


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == User.USER
        return False


class IsUserGet(permissions.BasePermission):

    def has_permission(self, request, view):
        methods = ('GET', 'PATCH')
        if not request.user.is_anonymous and request.method in methods:
            return True
        return False


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == User.MODERATOR
        return False


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == User.ADMIN
        return False


class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class AdminSuperUserOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class AdminSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'GET':
            return request.user.is_staff
        return True
