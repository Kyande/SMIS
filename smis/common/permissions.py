from rest_framework import permissions

from smis.users.models import ADMIN, SYSTEM_USER


class IsAdminOrSystemUser(permissions.BasePermission):
    """
    Persmission check for organisation admin system admin users.
    """
    message = (
        "This action is available for organisation admins or system admin")

    def has_permission(self, request, view):
        return bool(request.user.user_type in {ADMIN, SYSTEM_USER})
