from rest_framework.permissions import BasePermission

class IsAdminOrFleetManager(BasePermission):
    message = "Only Admin or Fleet Manager can manage drivers."
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in [
            "ADMIN",
            "FLEET_MANAGER",
        ]