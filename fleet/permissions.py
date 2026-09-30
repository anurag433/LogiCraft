from accounts.models import User
from rest_framework.permissions import BasePermission

class IsAdminOrFleetManager(BasePermission):
    message = (
        "Only admin or fleet manager can access "
        "fleet management."
    )
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.ADMIN,
                User.Role.FLEET_MANAGER,
            ]
        )
    






