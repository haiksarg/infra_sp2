from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Только админы могут совершать это действие"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """НЕ админы могут только читать"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """Вносить изменения могут автор, модератор и админ"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_authenticated and request.user.is_admin)
            or (request.user.is_authenticated and request.user.is_moderator)
        )
