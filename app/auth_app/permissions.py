from rest_framework.permissions import BasePermission
from auth_app.models import User, RolePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, User)


class RBACPermission(BasePermission):
    def has_permission(self, request, view):
        action = request.method
        resourse = view.resourse
        return RolePermission.objects.filter(
                role__userrole__user=request.user,
                permission__resource__name=resourse,
                permission__action__name=action
            ).exists()
