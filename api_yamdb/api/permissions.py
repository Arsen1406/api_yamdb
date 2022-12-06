from rest_framework import exceptions
from rest_framework import permissions
from reviews.models import User


class UserOrModeratorSelfGetPatchOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        request_username = str(
            request.parser_context['kwargs'].get('username')).lower()
        if request.user.is_anonymous:
            return False
        if (
                request.user.role in [User.USER, User.MODERATOR]
                and request_username == 'me'
                and request.method in ['GET', 'PATCH']
        ):
            return True
        elif (
                request.user.role in [User.USER, User.MODERATOR]
                and request_username == 'me'
                and request.method in ['DELETE']
        ):
            raise exceptions.MethodNotAllowed('DELETE')

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == User.ADMIN
        return False


class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'admin'


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'GET':
            return hasattr(request.user,
                           'role') and request.user.role == 'admin'
        return True


class ReviewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user or
                request.user.role == User.MODERATOR)
