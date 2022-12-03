from rest_framework import permissions

from reviews.models import User


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == User.ADMIN
        return False


class AdminSuperUserOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        role_admin_moder = ('SUPRUSER', 'ADMIN')
        if request.user.role in role_admin_moder:
            return True
        return False


class AutorizedOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role != 'ANONIMUS':
            return True
        return False
