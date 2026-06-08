from rest_framework.permissions import BasePermission
from auth_app.models import RolePermission, UserRole


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.id:
            return True
        return False


class RBACPermission(BasePermission):
    def has_permission(self, request, view):
        action = request.method
        resourse = view.resourse
        return RolePermission.objects.filter(
                role__userrole__user=request.user,
                permission__resource__name=resourse,
                permission__action__name=action
            ).exists()


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return UserRole.objects.filter(
            user=request.user,
            role__name='admin'
        ).exists()
