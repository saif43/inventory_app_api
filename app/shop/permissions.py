from rest_framework import permissions


class AccessPermission(permissions.BasePermission):
    """Allowing/Restricting user to update their profile"""

    def has_permission(self, request, obj):
        try:
            return request.user.is_superuser
        except:
            return False