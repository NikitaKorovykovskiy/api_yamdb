from rest_framework import permissions


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """
    Полные права доступа для Админа, Модератора и Владельца,
    для остальных только чтение
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                )


class IsSuperUser(permissions.BasePermission):
    """
    Доступ суперюзера
    """
    
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Полное разрешение для Админа,
    для остальных только чтение
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)





