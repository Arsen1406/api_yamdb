from rest_framework import permissions

from reviews.models import User


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == User.USER
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
        if request.user.is_authenticated and request.user.is_staff \
                or request.user.role == 'ADMIN':
            return True
        return False


# class GeneralPermission(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return bool(request.user.is_authenticated and
#                     (request.user.is_staff or
#                      request.user.role == UserRole.ADMIN) or
#                     request.method in permissions.SAFE_METHODS)
